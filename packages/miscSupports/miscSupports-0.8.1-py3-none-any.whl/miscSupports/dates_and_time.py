from datetime import datetime


def invert_dates(dates_list, delimiter="/"):
    """
    Returns dates of type dd-mmy-yyy into yyyymmdd

    :param dates_list: List of dates to invert, a string of a date to invert, or a datetime to invert
    :type dates_list: list[str] | str | datetime

    :param delimiter: The delimiter to split the string into [dd, mm, yyyy] if date is a str
    :type delimiter: str

    :return: list of inverted dates, or a string of an inverted date
    :rtype: list[str] | str
    """

    if isinstance(dates_list, str):
        day, month, year = [time.zfill(2) for time in dates_list.split(delimiter)]
        return year + month + day

    elif isinstance(dates_list, (list, tuple)):
        split_dates = [[time.zfill(2) for time in date.split(delimiter)] for date in dates_list]
        return [year + month + day for day, month, year in split_dates]

    elif isinstance(dates_list, datetime):
        return str(dates_list.year) + str(dates_list.month).zfill(2) + str(dates_list.day).zfill(2)

    else:
        raise TypeError(f"invert_dates expects a str, list, or tuple yet found {type(dates_list)}")


def restore_dates(inverted_dates):
    """
    This restores dates back to a datetime date from yyyymmdd.
    """
    if isinstance(inverted_dates, (str, int)):
        inverted_dates = str(inverted_dates)
        year, month, day = int(inverted_dates[:4]), int(inverted_dates[4:6]), int(inverted_dates[6:])
        return datetime(year, month, day)

    elif isinstance(inverted_dates, (list, tuple)):
        return [datetime(int(str(date)[:4]), int(str(date)[4:6]), int(str(date)[6:])) for date in inverted_dates]

    else:
        raise TypeError(f"restores_dates expects a str, list or tuple yet found {type(inverted_dates)}")


def terminal_time():
    """
    A way to remember when you initialised a cell by return the current hour and minute as a string
    """
    return f"{datetime.now().time().hour}:{datetime.now().time().minute}"


def date_prior(date, date_to_check):
    """
    Check to see if the date of birth is before or after the date to check
    """
    if date < date_to_check:
        return 0
    else:
        return 1


def within_date(date_min, date_max, current_date):
    """
    Test if a provided date is greater than or equal to a min date or less than max date
    """
    if date_min <= current_date < date_max:
        return True
    else:
        return False


def rebase_year(base_date, rebase_list):
    """
    Instead of working from jan-dec work from another month - month within a year.

    Lets say you have dates of birth based on january to december but actually want them to be based on september to
    august to model a disease session. By providing a list of datetime's that have the years of interest and then the
    month set to september you can rebase those born in the year after to the form to insure season are consistent.

    Example
    ---------
    For example lets say you have two individuals born in March and October 1944. If you are modeling a disease with
    non-gregorian calender seasonality of september to august then you want to ensure that individuals year fixed
    effects are consistent with seasons of disease rather than just the year they where born in. This method would put
    the individual born in March to now be born in the 1943 season of this disease, whilst the individual in October
    would remain in 1944.

    :param base_date: The original datetime date you want to rebase to another year
    :type base_date: datetime

    :param rebase_list: A list of datetime that you want to check that a date is between
    :type rebase_list: list[datetime]

    :return: The year of the year in the rebase list
    :rtype: int
    """
    for i, y in enumerate(rebase_list):
        if (i > 0) and (rebase_list[i - 1] <= base_date < y):
            return rebase_list[i - 1].year
