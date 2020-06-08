import pandas as pd
import numpy as np


def clean_weather_df(df):
    """ Clean weather data
    [Arg] df = pd.DataFrame
    [Return] df_clean = pd.DataFrame
    [Example] df_weather = data.clean_weather_df(df_weather)
    """
    # check if df is a pd.DataFrame
    assert isinstance(df, pd.DataFrame)

    df_clean = df.copy()

    # remove redundant columns
    columns_to_remove = ['wind_deg', 'rain_1h', 'rain_3h', 'snow_1h', 'snow_3h']
    df_clean.drop(columns_to_remove, axis=1, inplace=True)

    # filter datetime from 2018 to 2019-07-15 (KPI release)
    df_clean = df_clean[(df_clean['dt_iso'] >= np.datetime64('2018-01-01')) &
                        (df_clean['dt_iso'] < np.datetime64('2019-07-15'))]

    # add is_day column
    df_clean['is_daytime'] = df_clean['weather_icon'].str[-1].replace({'d': 1, 'n': 0})

    # check if there are duplicate datetimes
    if any(df_clean['dt_iso'].value_counts() > 1):
        print('clean_weather_df(): drop {} duplicates.'.format(sum(df_clean['dt_iso'].value_counts() > 1)))
        df_clean.drop_duplicates(subset='dt_iso', keep='first', inplace=True)

    return(df_clean)


if __name__ == "__main__":
    """
    """
    pass
