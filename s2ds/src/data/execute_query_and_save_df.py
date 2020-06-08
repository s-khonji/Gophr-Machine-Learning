import mysql.connector as sql
import pandas as pd
import os
import utils

def execute_query_and_save_df(
        query_filename,
        feather_filename = None, *,
        query_dir = utils.path_to('src', 'data'),
        feather_dir = utils.path_to('data', 'raw')
):
    """read SQL query from file, execute query, return pandas dataframe and
    optionally save pandas dataframe at given file path in feather format

    Arguments:
    query_filename (str): name of the query file
    feather_filename (str, optional): name of the feather file to write

    Keyword Arguments:
    feather_dir (str, optional): directory where the feather file is written
    query_dir  (str, optional): directory where the query is stored

    Returns:
    pd.DataFrame: pandas dataframe with the query result
    """

    print('Opening database connection')
    db_connection = sql.connect(
              host='35.233.4.203',
              user='s2ds',
              passwd='ier2rJZte8rt4fGHj2Sfi',
              database='s2ds'
    )

    query_filepath = os.path.join(query_dir, query_filename)
    print('Querying database with query in ' + query_filepath)
    query_string = utils.read_file_as_string(query_filepath)
    df = pd.read_sql(query_string, con=db_connection)

    print('Closing database connection')
    db_connection.close()

    if feather_filename is not None:
        feather_filepath = os.path.join(feather_dir, feather_filename)
        write_feather_file(df, feather_filepath)

    return df


def write_feather_file(df, feather_filepath):
    utils.ensure_directories(feather_filepath)
    print('Writing feather file to ' + feather_filepath)
    df.to_feather(feather_filepath)
    return df
