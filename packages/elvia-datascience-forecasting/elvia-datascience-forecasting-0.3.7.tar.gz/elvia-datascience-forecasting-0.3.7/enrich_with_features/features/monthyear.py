import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from pandas import DatetimeIndex


def monthyear(df: pd.DataFrame) -> pd.DataFrame:
    """
     This function adds day of week as a feature to the dataframe  and 
     returns just the new feature and substation_id as dataframe

     # Parameters
     --------------
     df: Dataframe with datetime index

     # Returns
     --------------
     pd.DataFrame
    
     """

    # Create months of of a year as a new feature (for example: 1-Januar, 12-December)
    initial_index: DatetimeIndex = df.index if isinstance(
        df.index, DatetimeIndex) else pd.to_datetime(df.index)
    df['monthyear'] = initial_index.month.astype(np.float32)

    return df
