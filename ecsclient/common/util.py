# Standard lib imports
import datetime

# Third party imports
# None

# Project level imports
# None


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
