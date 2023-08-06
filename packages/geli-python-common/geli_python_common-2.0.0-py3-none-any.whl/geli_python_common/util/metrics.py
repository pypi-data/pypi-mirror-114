from __future__ import absolute_import, division, print_function
"""
A file that tracks the same constants in Java. If you need to add something here
also make sure it is in the net.geli.dto.enums.DeviceMetric class

TBD Generate file based on the java source
"""


def _create_unit(label):
    return {"label": label}


def _create_metric(num, unit, desc):
    return {"id": str(num), "base_unit": unit, "description": desc}


class BaseUnit(object):
    NON_SCALAR = _create_unit(
        ""
    )  # unit that isn't a unit, for values that will be used "raw" e.g. bit extraction
    WATTS = _create_unit("W")  # true power
    WATTS_PER_SEC = _create_unit("W/s")  # power ramp rate
    VAR = _create_unit("VAR")  # reactive power
    VA = _create_unit("VA")  # apparent power
    AMPS = _create_unit("A")
    VOLTS = _create_unit("V")
    HERTZ = _create_unit("Hz")  # frequency
    WATT_HOURS = _create_unit("Wh")
    VAR_HOURS = _create_unit("VARh")
    VA_HOURS = _create_unit("VAh")
    SECONDS = _create_unit("s")
    MILLISECONDS = _create_unit("ms")
    RATIO = _create_unit(
        "")  # percentage  = _create_unit(as 0.00 - 1.00) or ratio
    COUNT = _create_unit("")  # qty/number of countable things
    METERS = _create_unit("M")
    METERS_PER_SEC = _create_unit(
        "M/s")  # velocity  = _create_unit(e.g. wind speed)
    TRUE_NORTH_BEARING = _create_unit(
        "dNorth")  # compass direction converted to true north
    WATTS_PER_M2 = _create_unit("W/m^2")  # watts per square meter; insolation
    TEMP_C = _create_unit("degC")  # temperature in Celsius
    BAR = _create_unit("bar")  # pressure  = _create_unit(e.g. barometer)
    GRAMS = _create_unit("g")
    DEGREES = _create_unit("deg")


class Metrics:
    INVALID_METRIC = _create_metric(0, BaseUnit.RATIO,
                                    "Invalid Metric")  # internal error

    # 1xxx single or multiphase power sensor port
    TRUE_POWER_TOTAL = _create_metric(1000, BaseUnit.WATTS,
                                      "True Power Total")  # true power "P"
    TRUE_POWER_A = _create_metric(1010, BaseUnit.WATTS, "True Power A")
    TRUE_POWER_B = _create_metric(1020, BaseUnit.WATTS, "True Power B")
    TRUE_POWER_C = _create_metric(1030, BaseUnit.WATTS, "True Power C")
    REACTIVE_POWER_TOTAL = _create_metric(
        1100, BaseUnit.VAR, "Reactive Power Total")  # reactive power "Q"
    REACTIVE_POWER_A = _create_metric(1110, BaseUnit.VAR, "Reactive Power A")
    REACTIVE_POWER_B = _create_metric(1120, BaseUnit.VAR, "Reactive Power B")
    REACTIVE_POWER_C = _create_metric(1130, BaseUnit.VAR, "Reactive Power C")
    APPARENT_POWER_TOTAL = _create_metric(
        1200, BaseUnit.VA, "Reactive Power Total")  # apparent power "S"
    APPARENT_POWER_A = _create_metric(1210, BaseUnit.VA, "Reactive Power A")
    APPARENT_POWER_B = _create_metric(1220, BaseUnit.VA, "Reactive Power B")
    APPARENT_POWER_C = _create_metric(1230, BaseUnit.VA, "Reactive Power C")

    FREQUENCY = _create_metric(1510, BaseUnit.HERTZ, "Frequency")
    POWER_FACTOR = _create_metric(1600, BaseUnit.RATIO, "Power Factor")
    ANGLE_CURRENT_A = _create_metric(1710, BaseUnit.DEGREES, "Angle Current A")
    ANGLE_CURRENT_B = _create_metric(1720, BaseUnit.DEGREES, "Angle Current B")
    ANGLE_CURRENT_C = _create_metric(1730, BaseUnit.DEGREES, "Angle Current C")
    ANGLE_V_AB = _create_metric(1750, BaseUnit.DEGREES, "Angle Volts A")
    ANGLE_V_BC = _create_metric(1760, BaseUnit.DEGREES, "Angle Volts B")
    ANGLE_V_CA = _create_metric(1770, BaseUnit.DEGREES, "Angle Volts C")

    # 2xxx single or multiphase voltage sensor port
    V_NEUTRAL_A = _create_metric(2010, BaseUnit.VOLTS, "Voltage A-N")
    V_NEUTRAL_B = _create_metric(2020, BaseUnit.VOLTS, "Voltage B-N")
    V_NEUTRAL_C = _create_metric(2030, BaseUnit.VOLTS, "Voltage C-N")
    V_AB = _create_metric(2110, BaseUnit.VOLTS, "Voltage A-B")
    V_BC = _create_metric(2120, BaseUnit.VOLTS, "Voltage B-C")
    V_CA = _create_metric(2130, BaseUnit.VOLTS, "Voltage C-A")

    # 3xxx single or multiphase current sensor port
    I_A = _create_metric(3010, BaseUnit.AMPS, "Current A")
    I_B = _create_metric(3020, BaseUnit.AMPS, "Current B")
    I_C = _create_metric(3030, BaseUnit.AMPS, "Current C")
    I_NEUTRAL = _create_metric(3100, BaseUnit.AMPS,
                               "Current N")  # neutral current

    # 4xxx accumulating energy meter port

    # energy in or energy net  = _create_metric(if negative, or if wh_out always 0, then net)
    ENERGY_IN_NET = _create_metric(4000, BaseUnit.WATT_HOURS,
                                   "Energy In or Net")
    ENERGY_OUT = _create_metric(4010, BaseUnit.WATT_HOURS, "Energy Out")

    # 5xxx inverter and/or BMS type device core
    STORED_ENERGY = _create_metric(5100, BaseUnit.WATT_HOURS,
                                   "Stored Energy")  # stored energy
    MIN_CHARGE = _create_metric(
        5110, BaseUnit.WATT_HOURS, "Minimum Stored Energy"
    )  # minimum stored energy  = _create_metric(less may be harmful)
    MIN_OP_CAPABILITY = _create_metric(5110, BaseUnit.WATT_HOURS,
                              "Minimum Operational Stored Energy")  # minimum stored energy
    CAPACITY = _create_metric(5120, BaseUnit.WATT_HOURS,
                              "Maximum Stored Energy")  # maximum stored energy
    MAX_OP_CAPABILITY = _create_metric(5115, BaseUnit.WATT_HOURS,
                              "Maximum Operational Stored Energy")  # maximum stored energy
    DERATE = _create_metric(
        5200, BaseUnit.RATIO, "Derate"
    )  # amount derated  = _create_metric(0=no derate, 1=completely off)
    CURTAIL = _create_metric(
        5300, BaseUnit.RATIO, "Curtail"
    )  # amount curtailed  = _create_metric(0=no curtail, 1=completely off)
    MAX_SOURCE = _create_metric(
        5610, BaseUnit.WATTS, "Hardware Maximum Source Power"
    )  # maximum power sourceable  = _create_metric(in grid direction)
    CUR_MAX_SOURCE = _create_metric(
        5510, BaseUnit.WATTS, "Current Maximum Source Power"
    )  # maximum power sourceable  = _create_metric(in grid direction)
    MAX_SINK = _create_metric(
        5620, BaseUnit.WATTS, "Hardware Maximum Sink Power"
    )  # maximum power sinkable  = _create_metric(from grid direction)
    CUR_MAX_SINK = _create_metric(
        5520, BaseUnit.WATTS, "Current Maximum Sink Power"
    )  # maximum power sinkable  = _create_metric(from grid direction)
    MAX_VA = _create_metric(5530, BaseUnit.VA, "Maximum Apparent Power")
    MAX_CURRENT = _create_metric(5540, BaseUnit.AMPS, "Maximum Current")

    AC_DC_EFFICIENCY = _create_metric(5630, BaseUnit.RATIO, "AC-DC Efficiency")
    DC_DC_EFFICIENCY = _create_metric(5640, BaseUnit.RATIO, "DC-DC Efficiency")


    YEARLY_CYCLE_COUNT = _create_metric(5130, BaseUnit.COUNT, "Yearly Cycle Count")
    COMMISSIONING_DATE = _create_metric(9010, BaseUnit.MILLISECONDS, "Commissioning Date")

    # 6xxx environment and weather device core
    TEMP_AMBIENT = _create_metric(6010, BaseUnit.TEMP_C,
                                  "Ambient Temperature")  # ambient temperature
    TEMP_MIN = _create_metric(
        6020, BaseUnit.TEMP_C,
        "Coldest Temperature Sensor")  # coldest core sensor temperature
    TEMP_MAX = _create_metric(
        6030, BaseUnit.TEMP_C,
        "Hottest Temperature Sensor")  # hottest core sensor temperature
    INSOL_HORIZ = _create_metric(
        6110, BaseUnit.WATTS_PER_M2,
        "Horizontal Insolation")  # instantaneous horizontal insolation
    INSOL_PLANE = _create_metric(
        6120, BaseUnit.WATTS_PER_M2, "In-plane Insolation"
    )  # instantaneous in-plane  = _create_metric(i.e. with PV) insolation
    WIND_SPEED = _create_metric(6200, BaseUnit.METERS_PER_SEC, "Wind Speed")
    WIND_DIRECTION = _create_metric(6210, BaseUnit.TRUE_NORTH_BEARING,
                                    "Bearing  = _create_metric(True North)")
    BAROMETRIC_PRESSURE = _create_metric(6300, BaseUnit.BAR,
                                         "Barometric Pressure")

    # site rules/aggregation
    SITE_RULES_SCHEDULE = _create_metric(6300, BaseUnit.BAR,
                                         "Barometric Pressure")
