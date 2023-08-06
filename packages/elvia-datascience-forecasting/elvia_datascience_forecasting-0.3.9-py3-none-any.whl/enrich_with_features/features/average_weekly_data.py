import pandas as pd  # type: ignore
import numpy as np  # type: ignore


def average_weekly_data(tab_data_set) -> pd.DataFrame:
    """
    This function takes into Azure dataset of the average weekly data  and 
    returns a pandas dataframe

    tab_data_set: Azure tabular dataset
    """
    data: pd.DataFrame = tab_data_set.to_pandas_dataframe()
    data['houroftheweek_average'] = data['houroftheweek_average'].astype(
        np.float32)

    return data
