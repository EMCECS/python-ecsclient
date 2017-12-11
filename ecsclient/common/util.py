import datetime
import logging
from jsonschema import validate, FormatChecker

log = logging.getLogger(__name__)


def get_formatted_time_string(year, month, day, hour, minute=None):
    """
    Validates input parameters: year, month, day, hour and minute
    and returns the timestamp if valid

    :param year: Four digit year
    :param month: The month
    :param day: The day
    :param hour: The hour
    :param minute: The minutes (optional)
    :return: Returns time stamp in yyyy-MM-dd'T'HH:mm if parameters are valid

    Throws:
        ValueError in case of invalid input
    """

    if minute:
        d = datetime.datetime(int(year), int(month), int(day), int(hour),
                              int(minute))
        return d.strftime("%Y-%m-%dT%H:%M")
    else:
        d = datetime.datetime(int(year), int(month), int(day), int(hour))
        return d.strftime("%Y-%m-%dT%H")


def is_valid_response(response, schema):
    """
    Returns True if the response validates with the schema, False otherwise

    :param response: The response returned by the API
    :param schema: The schema to validate with
    :returns: True if the response validates with the schema, False otherwise
    """
    try:
        validate(response, schema, format_checker=FormatChecker())
        return True
    except Exception as e:
        log.warning("Response is not valid: %s" % (e,))
        return False
