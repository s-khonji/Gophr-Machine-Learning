import pandas as pd
import numpy as np
import heapq
from sklearn.preprocessing import OneHotEncoder
from operator import attrgetter

import features
import utils

# instances of class CycleType in use
FEATURECYCLES = [features.CYCLE_YEAR, features.CYCLE_WEEK, features.CYCLE_DAY]

SECONDS_OF_ONE_HOUR = 60 * 60
MINUTES_OF_ONE_HOUR = 60


def generate_features(df):
    """generates features and interim variables, returns extended dataframe and list of feature_names

    Arguments:
        df (pd.DataFrame): source dataframe

    Returns:
        df (pd.DataFrame): dataframe with feature columns appended
        feature_names (list of str): list of feature_names
    """

    # add intermediate variables to original df
    df_intermediate = intermediate_variables(df)
    df = pd.concat([df, df_intermediate], axis=1)

    # encode features
    df_features, feature_names = feature_encoding(df, include_pass=False)
    df = pd.concat([df, df_features], axis=1)

    return df, feature_names


def feature_encoding(df, *, include_pass=True):
    """encodes features, requires interim variables, returns features dataframe and list of feature_names

    Arguments:
        df (pd.DataFrame): source dataframe
        include_pass (bool): if True, unchanged features are copied to the result dataframe
                             if False, unchanged features are ignored in the data

    Returns:
        df_features (pd.DataFrame): dataframe with features
        feature_names (list of str): list of feature_names
                              includes all features including unchanged features, thus not affected by include_pass flag

    """

    # unchanged feature list
    # These features are just copied in the feature dataframe if include_pass=True
    pass_feature_names = [
        'show_on_board', 'is_first_war_job',
        'temp', 'feels_like', 'humidity', 'wind_speed', 'clouds_all', 'is_daytime'
    ]

    # combine new feature dataframe
    df_features = pd.concat([

        # Add unchanged features
        _pass_features(df, pass_feature_names, include_pass=include_pass),

        # additional variables suitable as feature and for exploration
        _engineered_variables(df),

        # Log transform features
        _log_transform_features(df, colnames=[
            'distance',
            'initial_time_buffer', 'estimated_journey_time',
            'courier_earnings_calc',
            'size_min', 'size_med', 'size_max', 'weight', 'volume', 'size_min_max'
        ]),

        # One hot encoding, drop the first category (i.e. 0 for booleans)
        _one_hot_features(df, drop='first', colnames=[
            'is_food', 'is_fragile', 'is_liquid', 'is_not_rotatable', 'is_glass', 'is_baked',
            'is_flower', 'is_alcohol', 'is_beef', 'is_pork'
        ]),

        # One hot encoding, keep all categories
        _one_hot_features(df, colnames=[
            'vehicle_type', 'job_priority',
            'weather_cats',
            'earliest_pickup_time_month', 'earliest_pickup_time_day', 'earliest_pickup_time_hour',
            'pickup_zone', 'delivery_zone'
        ]),

        # Encode cyclic features
        _cyclic_features(df, colnames=['earliest_pickup_time'], cycletypes=FEATURECYCLES),
        _cyclic_features(df, colnames=['delivery_deadline'], cycletypes=[features.CYCLE_DAY])

    ], axis=1)

    # generate feature list
    # list of all feature names for further modeling purposes including unchanged features
    feature_names = df_features.columns.tolist()
    if not include_pass:
        feature_names = pass_feature_names + feature_names

    return df_features, feature_names


def intermediate_variables(df):
    # intermediate variables required for feature engineering but not features themselves

    #   year, month, day of datetime vars for exploration and subsequent one-hot-encoding
    df_out = _timed_categories(df, colnames=['earliest_pickup_time'], cycletypes=FEATURECYCLES)
    df_out = df_out.join(_timed_categories(df, colnames=['delivery_deadline'], cycletypes=[features.CYCLE_DAY]))

    #   weather recategorization
    weather_main_recat_dict = {
        'Clouds': 'clouds',
        'Clear': 'clear',
        'Rain': 'rain',
        'Haze': 'haze',
        'Mist': 'haze',
        'Drizzle': 'rain',
        'Snow': 'snow',
        'Fog': 'haze',
        'Thunderstorm': 'rain'
    }
    df_out['weather_cats'] = df['weather_main'].replace(weather_main_recat_dict)

    #   add consignment derivatives
    df_out['volume'] = df['size_x'] * df['size_y'] * df['size_z']
    # min, med, max
    df_out['size_min'] = df[['size_x', 'size_y', 'size_z']].min(axis=1)
    df_out['size_max'] = df[['size_x', 'size_y', 'size_z']].max(axis=1)
    # the medium, i.e. the second largest element
    df_out['size_med'] = df[['size_x', 'size_y', 'size_z']].apply(lambda x: heapq.nlargest(2, x)[1], axis=1)
    # sum of smallest and largest side of the consignment (used by the company Hermes to determine package classes)
    df_out['size_min_max'] = df_out['size_min'] + df_out['size_max']


    #   location derivatives
    df_out['pickup_zone'] = df['pickup_postcode_outer'].apply(features.zone_from_postcode)
    df_out['delivery_zone'] = df['delivery_postcode_outer'].apply(features.zone_from_postcode)

    #   add time derivatives in hours
    pickup_and_delivery_buffer = pd.Timedelta(minutes=20)
    df_out['initial_time_buffer'] = (
            df['delivery_deadline'] - df['earliest_pickup_time']
            - pd.to_timedelta(df['estimated_journey_time'], 'minutes') - pickup_and_delivery_buffer
    ).dt.total_seconds() / MINUTES_OF_ONE_HOUR


    #   add features from merging jobs history
    # if 'event' in df.columns:
    #   do some distance calculations...


    return df_out


def _engineered_variables(df):
    # additional variables suitable as feature and for exploration
    print('Engineering individual features')

    df_out = pd.DataFrame()

    df_out['is_morning_job'] = df['earliest_pickup_time'].dt.hour < 10
    df_out['is_evening_job'] = df['earliest_pickup_time'].dt.hour > 16
    df_out['is_scheduled_job'] = (df['date_started'] - df['date_booked']) >= pd.Timedelta(hours=1)

    return df_out


def _one_hot_features(df, colnames, *, drop=None):
    # create OneHotEncoder instance, fit and transform
    print('One hot encoding: ' + ', '.join(colnames))
    enc = OneHotEncoder(drop=drop)
    np_out = enc.fit_transform(df[colnames])
    df_out = pd.DataFrame(
        np_out.toarray().astype('int'),
        columns=enc.get_feature_names(colnames)
    )
    return df_out


def _cyclic_features(df, colnames, *, cycletypes):
    print('Cyclic encoding: ' + ', '.join(colnames))
    # create cyclic features
    # two features (sin, cos) for every combination of colnames X cycletypes
    df_out = pd.DataFrame()
    for col in colnames:
        for cycle in cycletypes:
            # column name prefix for result columns
            prefix = col + '_' + cycle.cycle_name + '_'
            # polar transformation of column
            df_out[prefix + 'sin'], df_out[prefix + 'cos'] = features.cyclic_from_datetime(df[col], cycle)
    return df_out


def _log_transform_features(df, colnames):
    LOG_MIN_THRESHOLD = 0
    print('Log transforming: ' + ', '.join(colnames))
    # log transform features
    df_out = pd.DataFrame()
    for col in colnames:
        col_min = df[col].min()
        const_add = 0
        # set minimum 1 for log transform variables with minimum below 1
        if col_min <= LOG_MIN_THRESHOLD:
            const_add = 1 - col_min
            print('Minimum of {} is less or equal to {}: {}, adding constant of {} prior to log.'.format(
                col, LOG_MIN_THRESHOLD, col_min, const_add
            ))
        df_out[col + '_log'] = np.log(df[col] + const_add)
    return df_out


def _pass_features(df, colnames, *, include_pass=True):
    print('Unchanged features: ' + ', '.join(colnames))
    # return unchanged columns of input dataframe if include_pass is True, empty dataframe otherwise
    df_out = pd.DataFrame()
    if include_pass:
        df_out = df[colnames]
    return df_out


def _timed_categories(df, colnames, *, cycletypes):
    print('Timed categorising: ' + ', '.join(colnames))
    # extract attributes of datetime vars
    df_out = pd.DataFrame()
    for col in colnames:
        for cycle in cycletypes:
            retriever = attrgetter(cycle.attribute)
            df_out['_'.join([col, cycle.section_name])] = retriever(df[col])

    return df_out


if __name__ == "__main__":
    df = pd.read_feather(utils.path_to('data', 'interim', 'clean.feather'))

    print('Use case 1: Add columns to original df')
    feature_df, feature_names = generate_features(df.head(100))

    print('\nUse case 2: Return only feature columns')
    intermediate_df = pd.concat([df.head(100), intermediate_variables(df.head(100))], axis=1)
    feature_df, feature_names = feature_encoding(intermediate_df)
