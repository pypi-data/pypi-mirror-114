from typing import Dict, Union

import dateutil
import json
from datetime import time
import attr

from geli_python_common.dto.constants import ConnectedSolutionsSeason, MarketRegions, MarketExchanges
from geli_python_common.util.constants import ObjectiveType, SGIP_CYCLES, ConstraintType, SECONDS_PER_MINUTE, DrProgram
from geli_python_common.util.utils import boolean_converter, convert_dict_with_python_types_to_dict_with_strings
from abc import ABC

import os
from logbook import Logger

logger = Logger(__name__)


@attr.s
class ObjectiveSchema(ABC):
    type = attr.ib(type=ObjectiveType)

    @staticmethod
    def get(type: ObjectiveType, config: Dict) -> "ObjectiveSchema":
        """
        Instantiates and returns a configuration schema for provided objective_type and objective_configs
        """
        mapping = {
            ObjectiveType.SGIP: SgipObjectiveSchema,
            ObjectiveType.DCM: DcmObjectiveSchema,
            ObjectiveType.TOU: TouObjectiveSchema,
            ObjectiveType.MARKETS: WholesaleMarketObjectiveSchema,
            ObjectiveType.FREQUENCY_RESPONSE: FrequencyResponseObjectiveSchema,
            ObjectiveType.DR: DRObjectiveSchema,
        }
        return mapping.get(type, DefaultObjectiveSchema)(type=type, **config)

    def to_json(self):
        configs = {k: v for k, v in self.__dict__.items() if k != 'type'}
        configs = convert_dict_with_python_types_to_dict_with_strings(input_dict=configs)
        return json.dumps(configs, separators=(",", ":"))

    def update_config_file(self):
        config = {}

        # read existing config file if it exists
        if os.path.isfile(ObjectiveSchema.config_file_name):
            with open(ObjectiveSchema.config_file_name, 'r') as f:
                config_string = f.read()
                if len(config_string) > 0:
                    config = json.loads(config_string)

        # write updated config to file
        with open(ObjectiveSchema.config_file_name, 'w+') as f:
            if self.type.value in config.keys():
                config[self.type.value] = self.__dict__
            else:
                config.update({self.type.name: self.__dict__})

            for objective, objective_configs in config.items():
                config[objective] = {k: v.isoformat() if isinstance(v, time) else v for k, v in
                                     objective_configs.items() if k != 'type'}

            f.write(json.dumps(config))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def convert_string_time_to_datetime_time(string_time):
    """
    Convert string to to datetime.time.
    :param string_time: <str> any format supported by dateutil.parser
    :return:
    """
    return dateutil.parser.parse(string_time).time()


@attr.s
class SgipObjectiveSchema(ObjectiveSchema):
    start_discharge = attr.ib(type=str)
    stop_discharge = attr.ib(type=str)
    sgip_meter_port_topic = attr.ib(type=str, default=None)
    cycle_count = attr.ib(type=int, default=SGIP_CYCLES, converter=int)
    allow_multiple_cycles = attr.ib(type=bool, default=False)
    # Enable consideration of GHG emissions in optimization for SGIP
    offset_ghg = attr.ib(type=bool, default=False, converter=boolean_converter)
    # $/kg CO2 for use in optimizer objective
    ghg_penalty = attr.ib(type=float, default=1.0, converter=float)
    type = attr.ib(default=ObjectiveType.SGIP)

    # TODO why not converter annotation?
    def __attrs_post_init__(self):
        self.start_discharge = convert_string_time_to_datetime_time(self.start_discharge)
        self.stop_discharge = convert_string_time_to_datetime_time(self.stop_discharge)


@attr.s
class WholesaleMarketObjectiveSchema(ObjectiveSchema):
    # exchange and region are used in order to subscribe coopt to CurrentMarketDataDto
    # https://growingenergylabs.atlassian.net/wiki/spaces/SD/pages/737050994/Market+connector+microservice+-+Client+usage+guide

    region = attr.ib(type=MarketRegions, converter=MarketRegions)
    exchange = attr.ib(type=MarketExchanges, converter=MarketExchanges)
    type = attr.ib(default=ObjectiveType.MARKETS)

    @region.validator
    def validate_region(self, attribute, region):
        if region not in MarketExchanges.get_exchange_regions(self.exchange):
            raise ValueError(region.name + ' is not a valid region for exchange ' + self.exchange.name)

    @property
    def unique_id(self):
        """
        It is possible that the coopt is aware of multiple exchanges for the same region or multiple regions for
        the same exchange, so use unique_id to correctly identify wholesale price data.
        """
        return f'{self.exchange.name.lower()}-{self.region.name.lower()}'


@attr.s
class DcmObjectiveSchema(ObjectiveSchema):
    type = attr.ib(default=ObjectiveType.DCM)
    prefer_full = attr.ib(type=bool, default=False, converter=boolean_converter)
    charge_buffer = attr.ib(type=float, default=None, converter=lambda x: float(x) if x else None)
    prioritize_today = attr.ib(type=bool, default=False, converter=boolean_converter)
    limit_overcharge = attr.ib(type=bool, default=True, converter=boolean_converter)


@attr.s
class TouObjectiveSchema(ObjectiveSchema):
    type = attr.ib(default=ObjectiveType.TOU)
    # to enable tou arbitrage to consider feed_in tariffs, set do_feed_in to True
    do_feed_in = attr.ib(type=bool, default=False, converter=boolean_converter)
    # $/kWh for use in compensating net energy exported to grid,
    # When non-zero, NSC charge included in objective
    nsc_price = attr.ib(type=float, default=0.0, converter=float)


@attr.s
class DefaultObjectiveSchema(ObjectiveSchema):
    value = attr.ib(default=True)


@attr.s
class FrequencyResponseObjectiveSchema(ObjectiveSchema):
    target_frequency = attr.ib(type=float)
    dead_band = attr.ib(type=float)
    droop = attr.ib(type=float)
    # number of seconds per frequency response interval
    interval = attr.ib(type=float, default=SECONDS_PER_MINUTE * 30)
    # $ compensated/kW/interval bid
    price = attr.ib(type=float, default=1.1)
    type = attr.ib(default=ObjectiveType.FREQUENCY_RESPONSE)


@attr.s
class DemandResponseSeasonalConfig:
    price = attr.ib(type=float)
    expected_events = attr.ib(type=int)


@attr.s
class DRObjectiveSchema(ObjectiveSchema):
    program = attr.ib(type=DrProgram, converter=DrProgram)
    resource = attr.ib(type=str)
    seasonal_configs = attr.ib(
        type=Dict[ConnectedSolutionsSeason, DemandResponseSeasonalConfig],
        default=attr.Factory(lambda: dict()),
        converter=lambda x: {ConnectedSolutionsSeason(k): DemandResponseSeasonalConfig(**v) for k, v in x.items()}
    )
    type = attr.ib(default=ObjectiveType.DR)


@attr.s
class ConstraintSchema(ABC):
    type = attr.ib(type=ConstraintType)

    @staticmethod
    def get(type: ConstraintType, config: Union[None, Dict]) -> "ConstraintSchema":
        """
        Instantiates and returns a configuration schema for provided constraint_type and constraint_configs
        """
        mapping = {
            ConstraintType.ITC: ITCConstraintSchema,
        }
        return mapping.get(type, DefaultConstraintSchema)(type=type, **config)

    def to_json(self):
        params = {k: v.isoformat() if isinstance(v, time) else v for k, v in self.__dict__.items() if k != 'type'}
        return json.dumps(params, separators=(",", ":"))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


@attr.s
class DefaultConstraintSchema(ConstraintSchema):
    value = attr.ib(type=float, converter=float)


@attr.s
class ITCConstraintSchema(ConstraintSchema):
    type = attr.ib(type=ConstraintType, converter=ConstraintType)
    value = attr.ib(default=True, converter=boolean_converter)

