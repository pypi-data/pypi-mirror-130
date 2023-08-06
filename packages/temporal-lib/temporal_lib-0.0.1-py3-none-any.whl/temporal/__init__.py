""" __init__.py for the temporal package. """
import datetime
from datetime import datetime as datetime_class
from dateutil.tz import tzutc



def date_to_iso_string(any_date):
    """
    Given a date, create an ISO String.  For example, 2021-12-26.
    """

    if not isinstance(any_date, datetime.date):
        raise Exception(f"Argument should be of type 'datetime.date', not '{type(any_date)}'")
    return any_date.strftime("%Y-%m-%d")


def get_system_datetime_now(time_zone):
    """
    Given a dateutil.tz Time Zone, return the current DateTime.
    """
    utc_datetime = datetime_class.now(tzutc())  # First, get the current UTC datetime.
    return utc_datetime.astimezone(time_zone)  # Next, convert to the time_zone argument.


def is_datetime_naive(any_datetime):
    """
    Returns True if the datetime is missing a Time Zone component.
    """
    if not isinstance(any_datetime, datetime_class):
        raise TypeError("Argument 'any_datetime' must be a Python datetime object.")

    if any_datetime.tzinfo is None:
        return True
    return False


def make_datetime_naive(any_datetime):
    """
    Takes a timezone-aware datetime, and makes it naive.
    """
    return any_datetime.replace(tzinfo=None)



def safeset(any_dict, key, value, as_value=False):
    """
    This function is used for setting values on an existing Object, while respecting current keys.
    """

    if not hasattr(any_dict, key):
        raise AttributeError(f"Cannot assign value to unknown attribute '{key}' in dictionary {any_dict}.")
    if isinstance(value, list) and not as_value:
        any_dict.__dict__[key] = []
        any_dict.extend(key, value)
    else:
        any_dict.__dict__[key] = value
