import datetime
from abc import ABC, abstractmethod
from enum import Enum, auto
import attr
import json
import copy
from logbook import Logger

from typing import Set, Dict, List, Union, Type
from enum import auto
from uuid import UUID

import numpy as np

from geli_python_common.dto.constants import PriceUnit
from geli_python_common.util.utils import all_subclasses, camel_to_snake, snake_to_camel
from geli_python_common.util.ts_utils import decode_timeseries_object, raw_timestamp_to_datetime
from geli_python_common.util.metrics import Metrics

from geli_python_common.util.constants import SECONDS_PER_HOUR, GeHost, FORECASTER_TYPE, ResourceType, \
                                              ObjectiveType, ConstraintType, AlgorithmParameterType, \
                                              MILLISECONDS_PER_SECOND, SITE_RULE_OVERRIDE, KILOWATTS_PER_MEGAWATT

from geli_python_common.util.objective_schema import ObjectiveSchema, ConstraintSchema
from geli_python_common.util.time import SiteTime

logger = Logger(__name__)

DTO_IDENTIFIER_KEY = '@dto'


class Dto(ABC):

    # TODO JT use mapper like https://docs.pylonsproject.org/projects/colander/en/latest/?

    @staticmethod
    def from_json(dto_json_string, site_time=SiteTime('UTC'), topic=None):
        """
        Parse a DTO string and instantiate the corresponding DTO subclass.
        :param dto_json_string: DTO JSON representation,
        e.g. '{"@dto":"Tel","timestamp":1504132747403,"metrics":{"1200":-56.0},"resource":"d/meter/p/out/s"}'
        :param topic resource for the DTO if applicable and not embedded in payload, e.g. d/meter/p/out/s
        :return: DTO subclass instance
        """

        def dto_class_for_identifier(identifier):
            """
            Returns the Dto sub-class for the given identifier, e.g. TelDto class for 'Tel'
            :param identifier: Dto name minus the 'Dto' suffix
            :return: class reference
            """
            subclasses = all_subclasses(Dto)
            try:
                dto_class = next(filter(lambda subclass: subclass.__name__.split('Dto')[0] == dto_type, subclasses))
            except StopIteration:
                raise ValueError(f"Unknown DTO type {identifier}")
            return dto_class


        if isinstance(dto_json_string, dict):
            # don't operate on the passed-in dictionary
            json_dic = copy.deepcopy(dto_json_string)
        else:
            json_dic = json.loads(dto_json_string)

        dto_type = json_dic.pop(DTO_IDENTIFIER_KEY)

        # for list DTO type return a list of DTOs
        if dto_type == 'List':
            return [Dto.from_json(json.dumps(list_element), site_time) for list_element in json_dic['items']]

        # convert DTO/Java camel case keys to snake case DTO class fields
        json_dic = {camel_to_snake(key): value for key, value in json_dic.items()}

        try:
            dto_object = dto_class_for_identifier(dto_type)(**json_dic)

        except TypeError as e:
            # filter out fields that are not part of the DTO definition
            dto_class = dto_class_for_identifier(dto_type)
            known_dto_fields = set(dto_class.__dict__.keys()) | set([attribute.name for attribute in dto_class.__attrs_attrs__])
            unexpected_dto_fields = set(json_dic) - known_dto_fields
            if len(unexpected_dto_fields) > 0:
                logger.warn("Received unexpected DTO fields for {0}: {1}".format(dto_type, unexpected_dto_fields))
                for field in unexpected_dto_fields:
                    del json_dic[field]
            try:
                dto_object = dto_class(**json_dic)
            except Exception as e:
                logger.warn(f'Failed to create DTO object from {dto_json_string}: {e}')

        if topic is not None:
            dto_object.resource = topic

        # When we load a DTO object from the wire, the types may be all
        # wrong. They might be a dict instead of a dto, or a timestamp instead
        # of a datetime. This loops through all the attrs defined attributes
        # and if a type metadata exists, does the conversion. This only happens
        # for ones coming from json, ones built in Python must have all the
        # correct types to begin with.
        for field in dto_object.__attrs_attrs__:
            existing = getattr(dto_object, field.name)
            result = None

            if field.metadata.get("type", None) == None:
                continue
            elif field.metadata.get("type", None) == "dto":
                if isinstance(existing, list):
                    result = [Dto.from_json(x, site_time) for x in existing]
                elif isinstance(existing, set):
                    result = {Dto.from_json(x, site_time) for x in existing}
                else:
                    result = Dto.from_json(existing, site_time) if existing != None else None

            elif field.metadata.get("type", None) == "timestamp":
                result = raw_timestamp_to_datetime(existing, site_time.time_zone) if existing != None else None

            elif field.metadata.get("type", None) == "timestamp_list":
                result = [raw_timestamp_to_datetime(ts, site_time.time_zone) for ts in existing]

            elif field.metadata.get("type", None) == "timeseries":
                result = parse_timeseries_points(existing, site_time)

            elif field.metadata.get("type", None) == "paramdict":
                result = parse_param_dict(existing, site_time)

            elif field.metadata.get("type", None) != None:
                raise Exception("Misunderstood DTO field.")

            setattr(dto_object, field.name, result)

        return dto_object

    def to_json(self):
        return json.dumps(self._to_dto_dict(), default=json_serialize, separators=(",", ":"))

    def _to_dto_dict(self, item_dict=None):
        json_fields = {}
        # remove 'Dto' suffix
        if self.__class__.__name__[-3:] == "Dto":
            json_fields[DTO_IDENTIFIER_KEY] = self.__class__.__name__[:-3]
        else:
            raise ValueError("Expect DTO class name to end in 'Dto'")

        # TODO JT needs to include __attrs_attrs__?
        if item_dict is None:
            item_dict = self.__dict__

        # filter out fields with value None or enums with value None
        json_fields.update({snake_to_camel(key): value for key, value in item_dict.items() if value is not None
                       and not (hasattr(value, 'value') and value.value is None)
                       and not (isinstance(value, list) and len(value) == 0)
                       and not (isinstance(value, dict) and len(value) == 0)})

        return json_fields


def json_serialize(object):
    # timestamp serialization to milliseconds
    if isinstance(object, datetime.datetime):
        return int(object.timestamp() * MILLISECONDS_PER_SECOND)

    # nested Dto
    if isinstance(object, Dto):
        return object._to_dto_dict()

    # enum
    if isinstance(object, Enum):
        if isinstance(object.value, auto):
            return object.name.lower()
        else:
            return object.value

    if isinstance(object, np.ndarray):
        return list(object)

    if isinstance(object, Scenario):
        return [object.probability, object.sample_path]

    if isinstance(object, DrBidCurve):
        return {"price": object.price, "quantity": object.quantity}


def parse_param_dict(param_dict, site_time):
    if param_dict is None:
        return None

    param_dtos = {}
    for key, value in param_dict.items():
        param_dtos[key] = Dto.from_json(value, site_time)
    return param_dtos


def parse_timeseries_points(ts_points_list, site_time):
    return [TimeSeriesPoint(raw_timestamp_to_datetime(point['ts'], site_time.time_zone), point['v']) for point in ts_points_list if "v" in point]


def list_float_converter(values: Union[list, np.ndarray]):
    """
    Casts all elements to floats, handling None entries and list
    """
    contains_element = values is not None and (isinstance(values, list) and values or isinstance(values, np.ndarray) and values.any())

    return [float(x) if x is not None else None for x in values] if contains_element else values


@attr.s
class ListDto(Dto):
    items = attr.ib(type= List[Type[Dto]])


@attr.s
class TimeSeriesPoint(object):
    ts = attr.ib()
    v = attr.ib()


@attr.s
class MessageForResource(ABC):
    """
    Tag for all DTOs that are intended for a particular resource that they need to provide as an attribute.
    """
    @abstractmethod
    def resource(self):
        """
        Subclasses need to implement the attribute resource
        """
        pass


@attr.s
class SiteDto(Dto):
    site_code = attr.ib(type=str)
    name = attr.ib(type=str)

    # address data
    street_address = attr.ib(type=str)
    city = attr.ib(type=str)
    state_or_province_code = attr.ib(type=str)
    zip_code = attr.ib(type=str)

    # geolocation data - do not include when submitting, unless also setting manualGeolocation to true
    center_latitude = attr.ib(type=float)
    center_longitude = attr.ib(type=float)
    manual_geolocation = attr.ib(type=bool)

    # timezone data - do not include when submitting, unless also setting manualTimeZone to true
    time_zone = attr.ib(type=str)
    manual_time_zone = attr.ib(type=bool)

    site_host = attr.ib(type=str, default=None)
    nodes = attr.ib(metadata={"type": "dto"}, default=None)
    aggregation_set_id = attr.ib(type=UUID, default=None)
    site_host_group = attr.ib(type=UUID, default=None)
    id = attr.ib(type=UUID, default=None)

    commissioned = attr.ib(type=int, default=None)
    status = attr.ib(type="SiteStatusDto", default=None)

    unit_designation = attr.ib(type=str, default=None)
    # e.g. "NZ"
    country_code_a2 = attr.ib(type=str, default=None)


@attr.s
class ForecasterConfigurationDto(Dto):
    resource = attr.ib(type=str)
    # TODO JT there should be a converter from metric-id to enum element (1510 -> FREQUENCY), the Metrics class is pretty terrible in general
    metric = attr.ib(type=int, converter=int)
    forecaster_type = attr.ib(type=Union[str, FORECASTER_TYPE], converter=FORECASTER_TYPE)
    host = attr.ib(type=Union[str, GeHost], converter=GeHost)


@attr.s
class ForecasterInstanceDto(Dto):
    configuration = attr.ib(type=ForecasterConfigurationDto, metadata={"type": "dto"})
    # contains address, time-zone etc.
    site = attr.ib(type=SiteDto, metadata={"type": "dto"})
    commit_hash = attr.ib(type=str)
    # TODO JT fields from the ForecasterConfigSchema like back-window length?
    meta_data = attr.ib(type=dict, default=None)


@attr.s
class Scenario:
    probability = attr.ib(type=float)
    # NaN might be passed as a string and must be cast to float
    sample_path = attr.ib(attr.Factory(list), converter=lambda values: [float(x) for x in values])

    @staticmethod
    def converter(scenario: Union["Scenario", List]):
        if isinstance(scenario, Scenario):
            return scenario
        elif isinstance(scenario, list) and len(scenario) == 2:
            return Scenario(probability=scenario[0], sample_path=scenario[1])
        else:
            raise ValueError(f"Cannot instantiate a Scenario from: {scenario}")


@attr.s
class ForecastDto(MessageForResource, Dto):
    time = attr.ib(metadata={"type": "timestamp"})
    function = attr.ib()
    # Convention that first scenario in list should be used for the representative sample_path
    scenarios = attr.ib(type=List[Union[List, Scenario]],
                        converter=lambda scenarios: [Scenario.converter(scenario=scenario) for scenario in scenarios])
    resource = attr.ib(default=None)
    metric_id = attr.ib(converter=int, default=Metrics.TRUE_POWER_TOTAL['id'])

    @property
    def representative_sample_path(self):
        # Convention that first scenario in list should be used for the representative sample_path
        return self.scenarios[0].sample_path

    @property
    def probability(self):
        return self.scenarios[0].probability

    @property
    def timestamps(self):
        return decode_timeseries_object(self.representative_sample_path, self.time, self.function, "forecast")


@attr.s
class CooptimizerConfigurationDto(Dto):

    host = attr.ib(type=Union[str, GeHost], converter=GeHost)

    objectives = attr.ib(converter=lambda objectives_dict: {
        ObjectiveType(objective_name): ObjectiveSchema.get(ObjectiveType(objective_name), objective_configs
        if isinstance(objective_configs, dict) else {"value": objective_configs})
        for objective_name, objective_configs in objectives_dict.items()},
                         default=attr.Factory(dict))

    constraints = attr.ib(converter=lambda constraints_dict: {
        ConstraintType(constraint_name): ConstraintSchema.get(ConstraintType(constraint_name), constraint_configs
        if isinstance(constraint_configs, dict) else {"value": constraint_configs})
        for constraint_name, constraint_configs in constraints_dict.items() if constraint_configs is not False},
                         default=attr.Factory(dict))

    algorithm_parameters = attr.ib(converter=lambda parameter_dict: {
        AlgorithmParameterType(key): value for (key, value) in parameter_dict.items()} if parameter_dict else {},
                                   default=attr.Factory(dict))


@attr.s
class CooptimizerInstanceDto(Dto):
    configuration = attr.ib(type=CooptimizerConfigurationDto, metadata={"type": "dto"})
    # contains address, time-zone etc.
    site = attr.ib(type=SiteDto, metadata={"type": "dto"})
    commit_hash = attr.ib(type=str)
    # placeholder for additional data that we might want to attach in the future
    meta_data = attr.ib(type=dict)

    def to_json(self):
        dto_copy = CooptimizerInstanceDto(configuration=CooptimizerConfigurationDto(host=self.configuration.host),
                                          site=self.site,
                                          commit_hash=self.commit_hash,
                                          meta_data=self.meta_data)

        dto_copy.configuration.objectives = {k.name.lower(): json.loads(v.to_json()) for k, v in self.configuration.objectives.items()}
        dto_copy.configuration.constraints = {k.name.lower(): json.loads(v.to_json()) for k, v in self.configuration.constraints.items()}
        dto_copy.configuration.algorithm_parameters = {k.name.lower(): v for k, v in self.configuration.algorithm_parameters.items()}

        json_string = super(CooptimizerInstanceDto, dto_copy).to_json()

        return json_string


@attr.s
class DcmThresholdsDto(Dto):
    """
    DTO containing the currently maintained DCM thresholds.
    """
    timestamp = attr.ib(metadata={"type": "timestamp"})
    # mapping from rate identifier (e.g. "3326464-18300547") to value in Watts
    # Rates that are active for current season and tou
    active_rates = attr.ib(type=Dict[str, float], factory=dict)
    # Rates that are active for current season, but not the current tou
    inactive_rates = attr.ib(type=Dict[str, float], factory=dict)

    @property
    def rates(self) -> Dict[str, float]:
        """
        Returns a dictionary of both active and inactive rates
        """
        return {**self.active_rates, **self.inactive_rates}


@attr.s
class OptimizationScheduleDto(MessageForResource, Dto):
    """
    Other than time, and function, all variables can be either be a list or a single value. If the value changes over
    the forecast horizon, then set it to a list. If the value does not change, set it to a single float.
    All lists must have the same length.
    """
    # Time is the first timestamp of the optimization schedule
    time = attr.ib(metadata={"type": "timestamp"})
    # function will be used to convert time from a single value to a list covering the entire horizon
    function = attr.ib(type=str)
    soc = attr.ib(default=None, type="np.ndarray[float]", converter=list_float_converter)
    power = attr.ib(default=None, type="np.ndarray[float]", converter=list_float_converter)
    load = attr.ib(default=None, type="np.ndarray[float]", converter=list_float_converter)
    modified_load = attr.ib(default=None, type="np.ndarray[float]", converter=list_float_converter)
    pv = attr.ib(default=None, type="np.ndarray[float]", converter=list_float_converter)
    # Dispatcher will discharge if net_load exceeds max_modified_load
    max_modified_load = attr.ib(default=None, type="np.ndarray[float]", converter=list_float_converter)
    # Dispatcher will not charge above this value (net_load + power < charge_threshold)
    charge_threshold = attr.ib(default=None, type=float, converter=lambda x: float(x) if x is not None else None)
    # Dispatcher will not discharge below this value (net_load + power > discharge_threshold)
    discharge_threshold = attr.ib(default=None, type=float, converter=lambda x: float(x) if x is not None else None)
    # Dispatcher will attempt to prevent grid from going beneath this value.
    # This will constrain discharging, and sometimes force charging
    lower_line_limit = attr.ib(default=None, type=float, converter=lambda x: float(x) if x is not None else None)
    # Mechanism for ignoring max_modified_load, charge_threshold, and discharge_threshold in order to force the
    # dispatcher to charge or discharge at a certain rate.
    dispatch_override = attr.ib(convert=SITE_RULE_OVERRIDE, default=None)
    frequency_response_bid = attr.ib(default=None, type="np.ndarray[float]", converter=list_float_converter)
    resource = attr.ib(type=str, default=None)


@attr.s
class CurrentMarketDataRequestDto(Dto):
    """
    This is the current-market-data request Dto sent to the microservice to get the current data (look-ahead day prices).
    The requester is typically the Cloud Geli Engine

    exchange_name: The exchange from where the data is pulled from. Ex: JEPX, NEM
    region: Geographic region for which the data is requested. In case of JEPX, there are 9 regions.
    eos_serial: EOS serial number
    module_id: module identifier, e.g. cooptimizer1
    """

    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)
    region = attr.ib(type=str, converter=lambda x: x.lower().capitalize() if x else None)
    exchange_name = attr.ib(type=str, converter=lambda x: x.upper() if x else None)


@attr.s
class HistoricMarketDataRequestDto(Dto):
    """
    This is market request Dto sent to the microservice to get the current data (look-ahead day price).
    The requester could be the Cloud Geli Engine or Geni (to display the plots)

    exchange_name: The exchange from where the data is pulled from. Ex: JEPX, NEM
    region: Geographic region for which the data is requested. In case of JEPX, there are 9 regions.
    eos_serial: EOS serial number
    module_id: module identifier, e.g. cooptimizer1
    start_datetime: Should be in Unix date time format in milliseconds
    end_datetime: Should be in Unix date time format in milliseconds
    time_resolution: time resolution in minutes (1-min, 30-min, 60-min etc)
    """

    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)
    region = attr.ib(type=str, converter=lambda x: x.lower().capitalize() if x else None)
    exchange_name = attr.ib(type=str, converter=lambda x: x.upper() if x else None)
    start_datetime = attr.ib(type=datetime)
    end_datetime = attr.ib(type=datetime)
    time_resolution = attr.ib(type=int, default=30)


@attr.s
class MarketData(Dto):
    """
    timestamps: unix timestamp
    price: price
    unit: $/KWhr or $/MWhr.
    """

    timestamps = attr.ib(type=list, default=None)
    price = attr.ib(type=list, default=None)
    unit = attr.ib(type=str, default=None)

    @property
    def price_per_kWh(self) -> List[float]:
        """
        Take the raw price, and convert it to a price per kWh
        """
        if PriceUnit(self.unit) == PriceUnit.dollars_per_kWh:
            return self.price
        elif PriceUnit(self.unit) == PriceUnit.dollars_per_MWh:
            return [p/KILOWATTS_PER_MEGAWATT for p in self.price]
        else:
            raise ValueError(f"Unit: {self.unit} is not currently supported")


@attr.s
class CurrentMarketDataDto(MarketData):
    """
    This is the Dto which gets deserialized into Json and sent to the consumer who has requested
    the current market data.
    """


@attr.s
class HistoricMarketDataDto(MarketData):
    """
    This is the Dto which gets deserialized into Json and sent to the consumer who has requested
    the historic market data.
    """


@attr.s
class WeatherRegistrationDto(Dto):
    """
    This is the Weather data registration request Dto sent to the microservice, to get the weather data at
    the configured intervals. The requester is typically the Geni UI

    site_id: site identifier
    latitude: latitude of the site
    longitude: longitude of the site
    eos_serial: EOS serial number
    module_id: module identifier, e.g. cooptimizer1
    current_weather_interval: interval at which the current weather data needs to be fetched
                              from the weather service provider and published.

    forecasted_weather_interval: interval at which the forecasted weather data needs to be fetched
                              from the weather service provider and published.

    first_telemetry_time: First telemetry of the site in UnixDateTime format in milliseconds.
                          Historical data for the site is fetched from first_telemetry_time to-date.
    """

    site_id = attr.ib(type=str)
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)
    latitude = attr.ib(type=float)
    longitude = attr.ib(type=float)
    first_telemetry_time = attr.ib(type=int)
    current_weather_interval = attr.ib(type=int, default=1)
    forecasted_weather_interval = attr.ib(type=int, default=60)
    field_selector = attr.ib(type=str, default=None)


@attr.s
class CurrentWeatherDataRequestDto(Dto):
    """
    This is the request Dto sent to the microservice to get the current weather data.
    The requester is typically the Cloud Geli Engine

    site_id: site identifier
    eos_serial: EOS serial number
    module_id: module identifier, e.g. cooptimizer1
    """

    site_id = attr.ib(type=str)
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)



@attr.s
class ForecastedWeatherDataRequestDto(Dto):
    """
    This is the request Dto sent to the microservice to get the forecasted weather data.
    The requester is typically the Cloud Geli Engine

    site_id: site identifier
    eos_serial: EOS serial number
    module_id: module identifier, e.g. cooptimizer1
    """

    site_id = attr.ib(type=str)
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)


@attr.s
class HistoricWeatherDataRequestDto(Dto):
    """
    This is the request Dto sent to the microservice to get the historic weather data.
    The requester is typically the Cloud Geli Engine

    site_id: site identifier
    eos_serial: EOS serial number
    module_id: module identifier, e.g. cooptimizer1
    start_datetime: Should be in UnixDateTime format in milliseconds
    end_datetime: Should be in UnixDateTime format in milliseconds
    time_resolution: time resolution in minutes (1-min, 30-min, 60-min etc)
    """

    site_id = attr.ib(type=str)
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)
    start_datetime = attr.ib(type=int)
    end_datetime = attr.ib(type=int)
    time_resolution = attr.ib(type=int, default=30)


@attr.s
class CurrentWeatherDataDto(Dto):
    """
    This is the Dto which gets deserialized into Json and sent to the consumer who has requested
    the current weather data.

    timestamps: unix timestamp
    apparent_temperature, humidity, cloudcover, windspeed, dni: Weather params
    """

    timestamp = attr.ib(type=int, default=None)
    apparent_temperature = attr.ib(type=float, default=None)
    humidity = attr.ib(type=float, default=None)
    cloudcover = attr.ib(type=float, default=None)
    windspeed = attr.ib(type=float, default=None)
    dni = attr.ib(type=float, default=None)
    temperature = attr.ib(type=float, default=None)
    icon = attr.ib(type=str, default=None)
    summary = attr.ib(type=str, default=None)
    sunriseTime = attr.ib(type=int, default=None)
    sunsetTime = attr.ib(type=int, default=None)

@attr.s
class ForecastedWeatherDataDto(Dto):
    """
    This is the Dto which gets deserialized into Json and sent to the consumer who has requested
    the forecasted weather data. This contains forecasted weather data for the next 24 hours

    timestamps: unix timestamp
    apparent_temperature, humidity, cloudcover, windspeed, dni: Weather params
    """
    timestamps = attr.ib(type=list, default=None)
    apparent_temperature = attr.ib(type=list, default=None)
    humidity = attr.ib(type=list, default=None)
    cloudcover = attr.ib(type=list, default=None)
    windspeed = attr.ib(type=list, default=None)
    dni = attr.ib(type=list, default=None)
    temperature = attr.ib(type=list, default=None)
    summary = attr.ib(type=list, default=None)


@attr.s
class HistoricWeatherDataDto(Dto):
    """
    This is the Dto which gets deserialized into Json and sent to the consumer who has requested
    the historic weather data. It consists of historic weather data for request period and resolution

    timestamps: unix timestamp
    apparent_temperature, humidity, cloudcover, windspeed, dni: Weather params
    """

    timestamps = attr.ib(type=list, default=None)
    apparent_temperature = attr.ib(type=list, default=None)
    humidity = attr.ib(type=list, default=None)
    cloudcover = attr.ib(type=list, default=None)
    windspeed = attr.ib(type=list, default=None)
    dni = attr.ib(type=list, default=None)


@attr.s
class VersionDto(Dto):
    timestamp = attr.ib(metadata={"type": "timestamp"})
    service = attr.ib(type=str)
    identifier = attr.ib(type=str)
    version = attr.ib(type=str)


@attr.s
class ConfigDto(Dto):
    timestamp = attr.ib(metadata={"type": "timestamp"})
    service = attr.ib(type=str)
    identifier = attr.ib(type=str)
    properties = attr.ib(type=dict)

    def __attrs_post_init__(self):
        # Obfuscate passwords (first and last letter, three stars in between)
        self.properties = {k: v[0] + '***' + v[-1] if 'PASSWORD' in k.upper() else v for k, v in self.properties.items()}

@attr.s
class K8sCreateGeRequestDto(Dto):
    serial = attr.ib(type=int, converter=int)
    module_id = attr.ib(type=str)
    app = attr.ib(type=str)

@attr.s
class K8sDeleteGeRequestDto(Dto):
    serial = attr.ib(type=int, converter=int)
    module_id = attr.ib(type=str)
    app = attr.ib(type=str)

@attr.s
class GHGEmissionDataDto(Dto):
    """
    Dto for sending the emission data.

    region: grid region.
    data_type: ACTUAL or FORECAST.
    points: time series containing the ghg emission values.
    """
    region = attr.ib(type=str)
    data_type = attr.ib(type=str)
    points = attr.ib(metadata={"type": "timeseries"})


@attr.s
class GHGRegistrationDto(Dto):
    """
    Dto sent to the microservice for registering with GHG service.

    site_id: site identifier
    eos_serial: EOS serial number
    module_id: module identifier
    region: grid region.
    data_type: CURRENT, FORECAST or ALL.
    """

    site_id = attr.ib(type=str)
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)
    region = attr.ib(type=str)
    data_type = attr.ib(type=str)


@attr.s
class GHGDeRegistrationDto(Dto):
    """
    Dto sent to the microservice for deregistering from GHG service.

    site_id: site identifier
    eos_serial: EOS serial number
    module_id: module identifier
    """

    site_id = attr.ib(type=str)
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)


@attr.s
class TouBandsRequestDto(Dto):
    """
    Dto sent to the microservice for requesting the tou band

    start_time: starting date for the request
    end_time: end date for the request
    tariff_json: tariff dictionary
    """
    start_time=attr.ib(type=int)
    end_time = attr.ib(type=int)
    tariff_json = attr.ib(type=dict)


@attr.s
class TouBandsDto(Dto):
    """
    return the dto as the response to the geni UI

    tou_bands_result: TOU BAND result
    """
    tou_bands_result = attr.ib(type=dict)


@attr.s
class K8sScaleRequestDto(Dto):
    """
    Dto sent to the kubernetes service for scaling the app.

    serial: eos serial.
    module_id: module id of the app to be scaled.
    app: app type. eg: predictor, trainer, cooptimizer.
    replicas: no. of apps to scale to.
    """
    serial = attr.ib(type=int, converter=int)
    module_id = attr.ib(type=str)
    app = attr.ib(type=str)
    replicas = attr.ib(type=int, default=1)


@attr.s
class AuditLogWriteDto(Dto):
    """
    Dto sent to the CTS for audit weather config
    user: user email id.
    reason: reason to update weather config
    dto: audit WeatherRegistrationDto
    timestamp: time of config changed
    """
    user = attr.ib(type=str)
    reason = attr.ib(type=str)
    dto = attr.ib(type=Dto, metadata={"type": "dto"})
    timestamp = attr.ib(type=int)


@attr.s
class WeatherDeRegistrationDto(Dto):
    """
    This is the Weather data de registration request Dto sent to the microservice, to unsubscribe from weather.

    site_id: site identifier
    eos_serial: EOS serial number
    module_id: module identifier, e.g. cooptimizer1
    """
    site_id = attr.ib(type=str)
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)


@attr.s
class DrEventDto(Dto):
    """
    This Dto provides information about a Demand Response Event. All demand response events have a start and end
    timestamp, and some additionally have prices and quantities. DrEventDto for the Connect Solution's Demand Response
    programs will not have a value for price or quantity, while DrEventDto for California DRAM / Leap sites will.g
    """
    start_timestamp = attr.ib(metadata={"type": "timestamp"})
    end_timestamp = attr.ib(metadata={"type": "timestamp"})
    price = attr.ib(default=None, type=float, converter=lambda x: float(x) if x is not None else None)
    quantity = attr.ib(default=None, type=float, converter=lambda x: float(x) if x is not None else None)

    @property
    def duration(self):
        """
        Returns number of hours that the DR Event spans
        """
        if self.start_timestamp != 0 and self.end_timestamp.minute != 59:
            raise NotImplementedError("Duration is only implemented for hourly DR Events")

        duration = (self.end_timestamp + datetime.timedelta(minutes=1)) - self.start_timestamp
        return duration.total_seconds() / SECONDS_PER_HOUR


@attr.s
class DrEventsRequestDto(Dto):
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)
    start_time = attr.ib(metadata={"type": "timestamp"})
    end_time = attr.ib(metadata={"type": "timestamp"})
    program = attr.ib(type=str, default=None)


@attr.s
class BaselineDto(Dto):
    """
    Dto sent to the co-optimizer peristence service for persisting.
    hour: time on which baseline data received from geliengine
    quantity: quantity
    """
    hour = attr.ib(metadata={"type": "timestamp"})
    quantity = attr.ib(default=None, type=float, converter=lambda x: float(x) if x is not None else None)


@attr.s
class HistoricBaselineRequestDto(Dto):
    """
    Historical BaselineDto request
    """
    eos_serial = attr.ib(type=str)
    module_id = attr.ib(type=str)


@attr.s
class HistoricBaselineDto(Dto):
    """
    Historical BaselineDto
    """
    baseline_weekday = attr.ib(type=List[BaselineDto], default=None)
    baseline_weekend = attr.ib(type=List[BaselineDto], default=None)


@attr.s
class DrBidCurve:
    """
    Bid curve for the bids.
    """
    price = attr.ib(default=None, type=float, converter=lambda x: float(x) if x is not None else None)
    quantity = attr.ib(default=None, type=float, converter=lambda x: float(x) if x is not None else None)

    @staticmethod
    def converter(dr_bid_curve: Union["DrBidCurve", dict]):
        if isinstance(dr_bid_curve, DrBidCurve):
            return dr_bid_curve
        elif isinstance(dr_bid_curve, dict):
            return DrBidCurve(price=dr_bid_curve['price'],
                              quantity=dr_bid_curve['quantity'])
        else:
            raise ValueError(f"Cannot instantiate a DrBidCurve from: {dr_bid_curve}")


@attr.s
class DrBidDto(Dto):
    """
    Bid dto having bid curve with the start and end timestamp.
    """
    start_timestamp = attr.ib(metadata={"type": "timestamp"})
    end_timestamp = attr.ib(metadata={"type": "timestamp"})
    bid_curve = attr.ib(type=List[DrBidCurve], converter=lambda curves: [DrBidCurve.converter(dr_bid_curve=curve) for curve in curves])


@attr.s
class DrBidsDto(Dto):
    """
    Dto for sending the bids dto.
    """
    bids = attr.ib(type=List[DrBidDto], metadata={"type": "dto"})
    program = attr.ib(type=str, default=None)


@attr.s
class DrRequestBidDto(Dto):
    """
    Bid dto having bid curve with the start and end timestamp.
    """
    start_timestamp = attr.ib(metadata={"type": "timestamp"})
    end_timestamp = attr.ib(metadata={"type": "timestamp"})
    program = attr.ib(type=str, default=None)
