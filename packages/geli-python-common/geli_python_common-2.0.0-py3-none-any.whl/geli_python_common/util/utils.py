import datetime
import importlib
import pkgutil
import re
import time
#from geliengine.common.ts_utils import raw_timestamp_to_datetime
from enum import Enum
from typing import Dict, Union

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


# def retrieve_current_time(current_tz='UTC', conversion_tz='UTC', time=time.time):
#     """
#     ``retrieve_current_time`` retrieves current time as a UTC timestamp and converts it into a time zone adjusted time stamp
#
#     :param current_tz: <str> representing current_tz as a timezone from the Olson TZ database, https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
#     :param conversion_tz: <str> representing conversion_tz as a timezone from the Olson TZ database, https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
#     :return: (utc_tcurrent,current_datetime)
#     """
#     utc_tcurrent = int(time())  # round to nearest second
#     tcurrent = raw_timestamp_to_datetime(utc_tcurrent, conversion_tz)
#     return (utc_tcurrent, tcurrent)


def camel_to_snake(name):
    """
    converts a camelCase string to a snake_case string
    """
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def snake_to_camel(name):
    """
    converts a snake_case string to a camelCase string
    """
    return re.sub('_.', lambda x: x.group()[1].upper(), name) if name else None


def all_subclasses(cls):
    """
    Recurse through inheritance tree to find all sub-classes
    :param cls: base-class
    :return: set of sub-classes
    """
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


def load_package_modules(package_reference, package_path):
    """
    Import all modules for the package specified by the path.
    :param package_reference: pass __package__
    :param package_path: pass os.path.dirname(__file__)
    :return:
    """
    for (module_loader, name, ispkg) in pkgutil.iter_modules([package_path]):
        importlib.import_module('.' + name, package_reference)


def resource_id_to_device_code(resource_id: str) -> str:
    """
    Strip out device code from full resource id.
        eg: 'd/test/p/out' = 'test'
    :param resource_id:
    """
    if resource_id is not None:
        return resource_id.lstrip(r'(?:d/|m/)').replace("/p/in", "").replace("/p/out", "")
    else:
        return None


def boolean_converter(arg):
    """
    Used as an attrs converter (primarily for conversion from a json to dto)
    """
    return arg.lower() == "true" if isinstance(arg, str) else bool(arg)


def convert_python_types_to_json(to_convert) -> Union[str, bool, int, float]:
    """
    Make `to_convert` json compatible
    """
    if isinstance(to_convert, Enum):
        converted = to_convert.name
    elif isinstance(to_convert, datetime.time):
        converted = to_convert.isoformat()
    elif isinstance(to_convert, Dict):
        converted = convert_dict_with_python_types_to_dict_with_strings(input_dict=to_convert)
    elif hasattr(to_convert, "__dict__"):
        converted = convert_dict_with_python_types_to_dict_with_strings(input_dict=to_convert.__dict__)
    else:
        converted = to_convert

    return converted


def convert_dict_with_python_types_to_dict_with_strings(input_dict: Dict) -> Dict:
    """
    Recursive function that iterates through all key-value pairings within the provided dictionary and replaces
    enums, times, and user defined obejects with strings.
    """
    return {convert_python_types_to_json(k): convert_python_types_to_json(v) for k, v in input_dict.items()}