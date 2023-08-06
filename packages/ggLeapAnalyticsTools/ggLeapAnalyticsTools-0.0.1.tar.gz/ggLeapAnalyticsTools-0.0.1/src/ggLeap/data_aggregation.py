from datetime import datetime

import pandas as pd

from . import helpers


def remove_dates(df: pd.DataFrame) -> pd.DataFrame:
    """ Remove dates from all datetimes in a dataframe

    TODO: Write remainder of docstring
    """
    
    new_records = []

    for i in range(len(df)):
        current_record = df.loc[i]
        date_string = current_record["Date"]
        dt = helpers.ggLeap_str_to_datetime(date_string)
        new_dt = helpers.remove_date_datetime(dt)
        current_record["Date"] = new_dt
        new_records.append(current_record)

    return pd.DataFrame(new_records)
