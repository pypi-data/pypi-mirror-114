import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from pandas import DatetimeIndex


def dayofweek(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function adds day of week as a feature to the dataframe  and 
    returns just the new feature and substation_id as dataframe

    # Parameters
    --------------
    df: Dataframe with datetime index

    # Returns
    --------------
    pandas.DataFrame
    
    """
    dayofweek_mapping = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 0}

    # Create day of week as a new feature (for example: 0-sunday, 6-saturday)
    initial_index: DatetimeIndex = df.index if isinstance(
        df.index, DatetimeIndex) else pd.to_datetime(df.index)
    df["dayofweek"] = initial_index.dayofweek.map(dayofweek_mapping).astype(
        np.float32)

    return df
