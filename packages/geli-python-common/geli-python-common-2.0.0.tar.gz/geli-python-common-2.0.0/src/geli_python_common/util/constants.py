from aenum import Enum, MultiValueEnum
from enum import auto

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
MILLISECONDS_PER_SECOND = 1000
KILOWATTS_PER_MEGAWATT = 1000
MAX_LOG_PAYLOAD_LENGTH = 300
# Number of cycles required to satisfy SGIP requirements.
SGIP_CYCLES = 130
MAX_RETRY_COUNT = 3

class ConstantsEnum(Enum):
    @classmethod
    def list_values(cls):
        return [item.value for item in cls]

    @classmethod
    def has_value(cls, value):
        return value in cls.list_values()


class CaseInsensitiveEnum(ConstantsEnum):
    @classmethod
    def _missing_value_(cls, name):
        for member in cls:
            if member.name.upper() == name.upper():
                return member

    def _generate_next_value_(name, start, count, last_values):
        return name


class CaseInsensitiveMultiEnum(MultiValueEnum):
    @classmethod
    def _missing_value_(cls, name):
        for member in cls:
            if member.name.upper() == name.upper():
                return member

    def _generate_next_value_(name, start, count, last_values):
        return name


class GeHost(CaseInsensitiveEnum):
    """
    Host where this GE application is executed on.
    """
    ON_PREM = auto()
    CLOUD_PROCESS = auto()


class FORECASTER_TYPE(CaseInsensitiveEnum):
    KNN = auto()
    RANDOM_FORESTS = auto()
    SINGLE_RANDOM_FOREST = auto()
    PRESCIENT = auto()  # Perfect forecast - only possible in sims
    SSDD = auto()  # use past backwindow as forecast (Same Series Different Day)
    NAIVE = auto()  # set forecast to zero


class ResourceType(CaseInsensitiveMultiEnum):
    BMS = 'bms', 'ess'
    LOAD = auto()
    NET_LOAD = auto()
    GRID = auto()
    PV = auto()
    METER = auto()
    BUS = auto()
    INV = auto()
    RELAY = auto()


class ObjectiveType(CaseInsensitiveEnum):
    DEMAND_NEUTRAL = "DEMAND_NEUTRAL"
    DCM = "DCM"
    TOU = "TOU"
    NO_EXPORT = "NO_EXPORT"
    SMOOTHING = "SMOOTHING"
    BATTERY_CYCLING = "BATTERY_CYCLING"
    SGIP = "SGIP"
    AC_CLIPPED_ENERGY = "AC_CLIPPED_ENERGY"
    CURTAILMENT_COST = "CURTAILMENT_COST"
    MARKETS = "MARKETS"
    FREQUENCY_RESPONSE = "FREQUENCY_RESPONSE"
    DR = "DEMAND_RESPONSE"


class ConstraintType(CaseInsensitiveEnum):
    # ITC stands for Investment Tax Credit, and is a federal tax incentive that provides a tax credit for up to 30%
    # of the battery cost. To qualify, the battery must be charged by a renewable at least 75% of the time.  Qualified
    # batteries receive a tax credit equal to (battery cost * % charged by renewable * .30)
    # For more information, visit https://www.nrel.gov/docs/fy18osti/70384.pdf
    ITC = auto()
    # Discharge floor is a minimum value that the battery cannot discharge to cause grid to be less than.
    # eg 1. If discharge floor is 0 kW, and the current load is 1 kW, then the battery cannot discharge > 1 kW
    # eg 2. If discharge floor is 0 kW, and the current load is -1 kW, then the battery cannot discharge at all
    # https://growingenergylabs.atlassian.net/wiki/spaces/analytics/pages/795639844/Discharge+Floor
    DISCHARGE_FLOOR = auto()
    # The lower line limit incentives the battery to keep the metered grid >= the specified value.
    # This can service 3 primary goals of customers: max export, xero net export, and min import
    # https://growingenergylabs.atlassian.net/wiki/spaces/analytics/pages/795672594/Lower+Line+Limit
    LOWER_LINE_LIMIT = auto()


class AlgorithmParameterType(CaseInsensitiveEnum):
    LOAD_SCALE = auto()


class SITE_RULE_OVERRIDE(ConstantsEnum):
    NONE = None
    POWER_OVERRIDE = 'power_override'
    OVERGEN_OVERRIDE = 'overgen_override'
    DISCHARGE_OVERRIDE = 'discharge_override'


class DrProgram(CaseInsensitiveEnum):
    CAISO = "CAISO"
    EVERSOURCE = "EVERSOURCE"
    NATIONAL_GRID = "NATIONAL_GRID"
