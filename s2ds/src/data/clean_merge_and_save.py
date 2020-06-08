import utils
import os
import pandas as pd
import data


def clean_merge_and_save(data_filename='df1.feather',
                         weather_filename='weather_df.feather',
                         save_as=None,
                         raw_dir=utils.path_to('data', 'raw'),
                         interim_dir=utils.path_to('data', 'interim')):
    """ Read and clean raw data, merge, and save DataFrame
    [Arg]   data_file_path
            weather_file_path
    """
    # read data
    df_data = pd.read_feather(os.path.join(raw_dir, data_filename))
    df_weather = pd.read_feather(os.path.join(raw_dir, weather_filename))

    # call clean function
    df_data = data.clean_dataframe_p1(df_data)

    df_weather = data.clean_weather_df(df_weather)

    # merge data
    df_concat = data.merge_df1_and_weather(df_data, df_weather)

    # save data
    if save_as is not None:
        feather_filepath = os.path.join(interim_dir, save_as)
        print('Writing feather file to {}'.format(feather_filepath))
        df_concat.to_feather(feather_filepath)

    return df_concat
