import pandas as pd
import arrow
import pytz

YEAR_1973_MILLIS = 100000000000
YEAR_9999_MILLIS = 253370764800000

from datetime import datetime, timedelta, time
from geli_python_common.util.constants import MILLISECONDS_PER_SECOND

from logbook import Logger

logger = Logger(__name__)

def decode_timeseries_object(values, timestamp, function, obj_type, exclusive=1):
    """
    :param value list of telemetry samples
    :param timestamp datetime object with proper timezone
    :param function algorithm function, e.g. L1M
    :param obj_type <str>: ["forecast", "backwindow"]
    :param exclusive <bool>: If 1, exclude timestamp in constructed timeseries.
                             If 0, include first timestamp
    :return:
    """
    num_obs = len(values)
    last_obs = pd.to_datetime(timestamp)

    if function[0] == "L":
        digit = int(function[1:-1])
        time_resolution = function[-1]

        timestamp_range = range(exclusive, num_obs + exclusive)
        if obj_type == 'forecast':
            if time_resolution == 'S':
                timestamps = [(last_obs + pd.DateOffset(seconds=digit * i)).to_pydatetime() for i in timestamp_range]
            elif time_resolution == 'M':
                timestamps = [(last_obs + pd.DateOffset(minutes=digit * i)).to_pydatetime() for i in timestamp_range]
            elif time_resolution == 'H':
                timestamps = [(last_obs + pd.DateOffset(hours=digit * i)).to_pydatetime() for i in timestamp_range]
            else:
                raise ValueError("Unknown time resolution %s", function)

        elif obj_type == 'backwindow':
            if time_resolution == 'S':
                timestamps = [(last_obs + pd.DateOffset(seconds=-digit * i)).to_pydatetime() for i in timestamp_range]
            elif time_resolution == 'M':
                timestamps = [(last_obs + pd.DateOffset(minutes=-digit * i)).to_pydatetime() for i in timestamp_range]
            elif time_resolution == 'H':
                timestamps = [(last_obs + pd.DateOffset(hours=-digit * i)).to_pydatetime() for i in timestamp_range]
            else:
                raise ValueError("Unknown time resolution %s", function)
    else:
        raise ValueError(
            "Cannot decode time series forecast object with function type: " +
            str(obj_type))

    if len(timestamps) != num_obs:
        raise ValueError("Timestamps and telemetry values are misalligned")

    return timestamps


def raw_timestamp_to_datetime(raw_utc_timestamp, timezone):
    """
    convert utc timestamps to timezone-aware datetime timestamps
    :param raw_utc_timestamp: <int>
    :param timezone: <str> e.g. 'US/Pacific
    :return: <datetime>
    """
    if timezone is None:
        raise ValueError("Timezone needs to be specified")

    if isinstance(raw_utc_timestamp, datetime):
        return arrow.get(raw_utc_timestamp, timezone).datetime

    if not isinstance(raw_utc_timestamp, (int, float)):
        try:
            raw_utc_timestamp = float(raw_utc_timestamp)

        except Exception:
            raise ValueError(
                "Expect int or float timestamp in seconds or milliseconds, not {0}".format(
                    raw_utc_timestamp.__class__))

    if raw_utc_timestamp < YEAR_1973_MILLIS:
        # assume seconds, if millisecond timestamp would be before March 3, 1973 9:46:40 AM
        # (seconds surpass value Wed, 16 Nov 5138)
        converted_datetime = arrow.get(raw_utc_timestamp).to(timezone).datetime
    else:
        # limit to the year 9999 to prevent out of range ValueError
        if raw_utc_timestamp > YEAR_9999_MILLIS:
            logger.warn("Timestamp %s was limited to 9999 years" % raw_utc_timestamp)
            raw_utc_timestamp = YEAR_9999_MILLIS

        converted_datetime = arrow.get(raw_utc_timestamp / MILLISECONDS_PER_SECOND).to(timezone).datetime

    return converted_datetime


def to_epoch_seconds(datetimeobj):
    tz = pytz.UTC
    epoch_0 = tz.localize(datetime.utcfromtimestamp(0))
    return int((datetimeobj.astimezone(tz) - epoch_0).total_seconds()) if datetimeobj else None


def to_epoch_milliseconds(datetimeobj):
    return to_epoch_seconds(datetimeobj) * 1000 if datetimeobj else None
