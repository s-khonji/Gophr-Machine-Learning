import numpy as np
import calendar

SECONDS_OF_ONE_DAY = 24 * 60 * 60


class CycleType:
    """class of cycle types that provide a template for processing further or plotting

    Keyword Arguments:
        name (str): Name of the cycle type
        duration (int): Duration of the cycle in seconds
        labels (list of str): List of plot labels
        angles (list of int, optional): Angles to place the plot labels. Defaults to even distribution
        seconds (function): Function yielding the second in the cycle of a pandas datetime object
    """
    def __init__(self, *, cycle_name, section_name, attribute, duration, labels, angles=None, seconds):
        self.cycle_name = cycle_name
        self.section_name = section_name
        self.attribute = attribute
        self.duration = duration
        self.labels = labels
        self.angles = angles
        if self.angles is None:
            self.angles = np.degrees(np.linspace(.0, 2 * np.pi, len(self.labels), endpoint=False))
        self.seconds = seconds


def second_of_the_day(dt_object):
    """second of the day of a datetime object

    Argument:
        dt_object (pandas datetime object)

    Returns:
        pandas series of int
    """
    return dt_object.dt.second + (dt_object.dt.minute * 60) + (dt_object.dt.hour * 3600)


def second_of_the_year(dt_object, delete_feb_29=False):
    """second of the year of a datetime object

    Argument:
        dt_object (pandas datetime object)
        delete_feb_29 (bool, optional): flag if Feb 29 of a leap year should be deleted to simplify yearly plots

    Returns:
        pandas series of int
    """
    s = (dt_object.dt.dayofyear - 1) * SECONDS_OF_ONE_DAY + second_of_the_day(dt_object)
    if delete_feb_29:
        s[dt_object.dt.is_leap_year & dt_object.dt.month > 2] -= SECONDS_OF_ONE_DAY
        s = s[~((dt_object.dt.month == 2) & (dt_object.dt.day == 29))]
    else:
        # if the year is a leap year, squeeze one day in seconds
        s = (s * 365/(dt_object.dt.is_leap_year.astype('int') + 365)).astype('int')
    return s


def month_lengths(year=2018):
    """list of month lengths in days of a given year

    Argument:
        year (pandas datetime object)

    Returns:
        list of int: month lengths
    """
    return [calendar.monthrange(year, x + 1)[1] for x in range(12)]


CYCLE_DAY = CycleType(
    cycle_name='day',
    section_name='hour',
    attribute='dt.hour',
    duration=SECONDS_OF_ONE_DAY,
    labels=range(24),
    seconds=lambda x: second_of_the_day(x)
)

CYCLE_WEEK = CycleType(
    cycle_name='week',
    section_name='day',
    attribute='dt.weekday',
    duration=SECONDS_OF_ONE_DAY * 7,
    labels=calendar.day_abbr,  # unabridged would be calendar.day_name
    seconds=lambda x: x.dt.weekday * SECONDS_OF_ONE_DAY + second_of_the_day(x)
)

CYCLE_YEAR = CycleType(
    cycle_name='year',
    section_name='month',
    attribute='dt.month',
    duration=SECONDS_OF_ONE_DAY * 365,
    labels=calendar.month_abbr[1:],  # unabridged would be calendar.month_name[1:]
    # degrees depending on each months length, dropping 360 and prepending 0
    angles=np.insert(np.cumsum(month_lengths()[:-1]), 0, 0) / 365 * 360,
    seconds=lambda x: second_of_the_year(x, delete_feb_29=True)
)
