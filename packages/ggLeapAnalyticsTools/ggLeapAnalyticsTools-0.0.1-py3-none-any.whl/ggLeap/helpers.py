from datetime import datetime, date

def remove_date_datetime(dt: date) -> date:
    """ Remove a date from a datetime. """
    dt = dt.replace(year=1, month=1, day=1)
    return dt


def ggLeap_str_to_datetime(string: str) -> date:
    date = datetime.strptime(string,
                             "%m/%d/%Y %I:%M:%S %p")
    return date
