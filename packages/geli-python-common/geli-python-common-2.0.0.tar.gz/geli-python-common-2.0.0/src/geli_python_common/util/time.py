import attr
import arrow
import datetime
from geli_python_common.util.ts_utils import raw_timestamp_to_datetime

@attr.s
class SiteTime(object):
    """
    SiteTime is responsible for maintaining the time zone of the site.
    """
    # should be a string. To see complete list of options please refer to database
    # listed on https://www.iana.org/time-zones
    time_zone = attr.ib()

    def now(self):
        return arrow.now(self.time_zone).datetime

    def get(self, *args, **kwargs):
        """
        Get a datetime in the correct timezone.

        This mirrors the datetime API -- use like:

            get(1990, 1, 1)

        ...or...

            get(year=1990, month=1, day=1, hour=10, minute=20)
        """
        return arrow.get(datetime.datetime(*args, **kwargs), self.time_zone).datetime

    def from_unix(self, unix_timestamp: int) -> datetime.datetime:
        """
        Convert unix to datetime.
        """
        return raw_timestamp_to_datetime(unix_timestamp, self.time_zone)

    def from_datetime(self, ts: datetime.datetime) -> datetime.datetime:
        """
        Localize provided datetime to self.time_zone
        """
        # ts.timetuple() returns a struct_time (https://docs.python.org/2/library/time.html#time.struct_time)
        # site_time requires the first 6 elements of struct_time to create a valid datetime
        return self.get(*ts.timetuple()[:6])

    def from_string(self, ts: str, datetime_format="YYYY-MM-DD HH:mm") -> datetime.datetime:
        """
        get datetime from string
        """
        return self.get(*arrow.get(ts, datetime_format).timetuple()[:6])