import pandas as pd


def merge_df1_and_weather(df_data, df_weather):
    """ Merge data and the weather DataFrame
    [Arg] df_data = pd.DataFrame
          df_weather = pd.DataFrame
    [Return]  df_complete = pd.DataFrame
    [Example] df = data.merge_df1_and_weather(df_data, df_weather)
    """
    # check if df_data and df_weather are pd.DataFrame
    assert isinstance(df_data, pd.DataFrame)
    assert isinstance(df_weather, pd.DataFrame)

    # left join of df_data and df_weather on daytime rounded to hours (H)
    df_complete = df_data.merge(df_weather,
                                how='left',
                                left_on=df_data['insertion_date'].dt.round('H'),
                                right_on=df_weather['dt_iso'])

    # check if no rows were added
    assert (df_data.shape[0] == df_complete.shape[0])

    # drop key column
    column_to_drop = ['key_0']
    df_complete.drop(column_to_drop, axis=1, inplace=True)

    return(df_complete)


if __name__ == "__main__":
    """
    """
    pass
