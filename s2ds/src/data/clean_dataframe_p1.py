import pandas as pd
import numpy as np
import re
import string
import utils


def clean_dataframe_p1(df):
    """ clean the DataFrame for phase 1
    [Arg] pd.DataFrame
    [Return]  pd.DataFrame
    [Example] df_clean = data.clean_dataframe_p1(df)
    """

    # check duplicate id and if id equal job_id to drop one
    assert df['job_id'].drop_duplicates().count() == df['job_id'].count()
    assert (df['id'] == df['job_id']).any()

    col_dict = {'col_to_remove': ['id', 'event', 'date_accepted', 'date_picked_up', 'pickup_deadline',
                                  'hero_ratio', 'war_job_id', 'delivery_city', 'pickup_city',
                                  'final_price_net_calc', 'final_price_net_booked', 'courier_earnings_booked',
                                  'available_in_job_board', 'taken_from_job_board', 'assigned_manually'],
                'col_fillna_int': ['is_food', 'is_fragile', 'is_liquid', 'is_not_rotatable', 'is_glass',
                                   'is_baked', 'is_flower', 'is_alcohol', 'is_beef', 'is_pork'],
                'col_remove_neg': [],  # 'courier_money_earned_net' would delete 5000 cases
                'col_keep_na': ['pickup_postcode_inner', 'delivery_postcode_inner',
                                'canceled_status', 'canceled_reason'],
                'col_to_int': ['is_food', 'is_fragile', 'is_liquid', 'is_not_rotatable', 'is_glass', 'is_baked',
                               'is_flower', 'is_alcohol', 'is_beef', 'is_pork', 'accepted_count', 'rejected_count']}

    # copy data
    df_clean = df.copy()

    # filter war_job_id to keep only missing-values
    df_clean = df_clean[df_clean['war_job_id'].isnull()]
    # filter datetime from 2018 to 2019-07-15 (KPI release)
    df_clean = df_clean[(df_clean['insertion_date'] >= np.datetime64('2018-01-01')) &
                        (df_clean['insertion_date'] < np.datetime64('2019-07-15'))]

    # remove redundant columns
    df_clean.drop(col_dict['col_to_remove'], axis=1, inplace=True)

    # clean postcodes
    df_pickup_postcode = _clean_postcode(df_clean['pickup_postcode'])
    df_pickup_postcode.columns = 'pickup_' + df_pickup_postcode.columns
    df_clean = df_clean.join(df_pickup_postcode, how='right')  # how='right' drops all rows not in df_pickup_postcode

    df_delivery_postcode = _clean_postcode(df_clean['delivery_postcode'])
    df_delivery_postcode.columns = 'delivery_' + df_delivery_postcode.columns
    df_clean = df_clean.join(df_delivery_postcode, how='right')

    # for compatibility
    df_clean.rename(columns={
        'pickup_outcode': 'pickup_postcode_outer',
        'pickup_incode': 'pickup_postcode_inner',
        'delivery_outcode': 'delivery_postcode_outer',
        'delivery_incode': 'delivery_postcode_inner',
    }, inplace=True)

    # replace missing values in not-required columns with a special character 99
    df_clean[col_dict['col_fillna_int']] = df_clean[col_dict['col_fillna_int']].fillna(99)
    # replace missing value in is_first_war_job with a zero
    df_clean['is_first_war_job'] = df_clean['is_first_war_job'].fillna(0).astype('int')

    current_rows = df_clean.shape[0]
    print('')
    # remove any additional missing value except the ones listed in col_keep_na
    cols_to_check = df_clean.columns[~df_clean.columns.isin(col_dict['col_keep_na'])]
    for col in cols_to_check:
        del_pattern = df_clean[col].isna()
        if del_pattern.sum() > 0:
            print('Deleting {} rows with NAs in {}'.format(del_pattern.sum(), col))
            df_clean = df_clean[~del_pattern]

    print('clean_dataframe_p1(): {} rows with na removed.'.format(current_rows - df_clean.shape[0]))

    # remove rows with negative and zero values for log transform candidates
    for col in col_dict['col_remove_neg']:
        del_pattern = df_clean[col] <= 0
        if del_pattern.sum() > 0:
            print('Deleting {} rows with Zero or negative entries in {}'.format(del_pattern.sum(), col))
            df_clean = df_clean[~del_pattern]

    # handling data types
    df_clean[col_dict['col_to_int']] = df_clean[col_dict['col_to_int']].astype('int')

    # Treat cases with status 80 as rejected
    # accepted_count may be > 0, even if the job was cancelled (status is 80 and canceled_reason exists)
    # So 190 cases with canceled_reason 'NOT_ACCEPTED' and accepted_count > 0 also count as rejected
    df_clean.loc[df_clean['status'] == 80, 'abs_accepted_rejected'] = 'abs_rejected'

    # Add target column
    df_clean['is_accepted'] = df_clean['abs_accepted_rejected'].replace({'abs_accepted': 1, 'abs_rejected': 0})
    df_clean['is_rejected'] = df_clean['abs_accepted_rejected'].replace({'abs_accepted': 0, 'abs_rejected': 1})
    df_clean.drop('abs_accepted_rejected', axis=1, inplace=True)

    # keep only records if 'canceled_reason' is 'NOT_ACCEPTED' or None
    current_rows = df_clean.shape[0]
    df_clean = df_clean[df_clean['canceled_reason'].isin(['NOT_ACCEPTED', None])]
    print('clean_dataframe_p1(): {} rows with other ''canceled_reason'' entries removed.'.format(current_rows - df_clean.shape[0]))
    # Add target column 'is_hard'
    THRESHOLD = 5
    df_clean['is_hard'] = (df_clean['rejected_count'] > THRESHOLD).astype('int')
    # if 'canceled_reason' is 'NOT_ACCEPTED' set 'is_hard' to 1
    df_clean.loc[df_clean['canceled_reason'] == 'NOT_ACCEPTED', 'is_hard'] = 1

    return(df_clean)


def _clean_postcode(str_series, clean=True):
    """ Clean postcodes
    """
    print('\nRecoding postcodes in ' + str_series.name)
    # Regex and char constants
    # Chars to remove from series
    REMOVE_CHARS = string.whitespace + string.punctuation
    # Regex pattern for remove chars
    REMOVE_PATTERN = r"[{}]".format(REMOVE_CHARS)

    # see https://www.getthedata.com/postcode for UK postcode structure
    # see https://en.wikipedia.org/wiki/London_postal_district and subsequent pages for London postcodes

    # Regex pattern of an outcode in London
    PATTERN_OUTCODE_LONDON_STRICT = \
        '^(?P<outcode>EC(?:[1-4][AMNPRVY]|50)|WC[1-2][ABEHNRVX]|' + \
        'NW(?:[1-9][01W]?|26)|N(?:[1-9][0-9CP]?|81)|E(?:1[0-8W]?|[2-9]|20|77|98)|SE[1-9][0-9P]?|' + \
        'SW[1-9][0-9AEHPVWXY]?|W[1-9][0-4ABCDFGHJKSTUW]?)'
    #   We have to loosen the pattern to account for outcodes no longer in use (e.g. W1V)
    PATTERN_OUTCODE_LONDON = \
        '^(?P<outcode>EC(?:[1-4][A-Z]?|50)|WC[1-2][A-Z]?|' + \
        'NW(?:[1-9][01W]?|26)|N(?:[1-9][0-9CP]?|81)|E(?:1[0-8W]?|[2-9]|20|77|98)|SE[1-9][0-9P]?|' + \
        'SW[1-9][0-9A-Z]?|W[1-9][0-4A-Z]?)'

    # Regex pattern of an incode in UK
    PATTERN_INCODE_STRICT = '(?P<incode>(?P<sector>[0-9])(?P<unit>[A-Z]{2}))'
    #   Again, we have to loosen the pattern to account for typos
    #   and allow letters in the sector and numbers in the unit
    #   Quite common: Sometimes the incode contains a O instead of 0
    PATTERN_INCODE = '(?P<incode>(?P<sector>[0-9A-Z])(?P<unit>[0-9A-Z]{2}))'

    # Regex pattern for an Area in UK
    PATTERN_AREA = '^([A-Z]{1,2})(?=[0-9])'
    # Regex pattern for an Area in London, subset of PATTERN_AREA
    PATTERN_AREA_LONDON = '^(?:EC|WC|NW|N|E|SE|SW|W)(?=[1-9])'

    # We allow combinations of outcode + incode, outcode without incode and outcode + literal 'UK'
    # If given, the incode must consist of 3 characters to be considered as valid
    VALID_POSTCODE = re.compile(PATTERN_OUTCODE_LONDON + '(?:' + PATTERN_INCODE + '?|UK|)$')

    # capitalize postcodes
    str_series = str_series.str.upper()
    # remove whitespace and punctuation
    str_series = str_series.str.replace(REMOVE_PATTERN, '')

    # special treatment - 148 cases of W18 3AG which probably is W1B 3AG
    str_series = str_series.str.replace('^W183AG$', 'W1B3AG')

    # extract the postcode area
    district = str_series.str.extract(PATTERN_AREA, expand=False)
    # boolean var if it's a London area
    is_london = str_series.str.contains(PATTERN_AREA_LONDON)
    # split the postcode in outcode and incode, sector and unit
    postcode_df = str_series.str.extract(VALID_POSTCODE)
    postcode_df.drop(columns=['sector', 'unit'], inplace=True)  # sector and unit dropped, not in use
    postcode_df = pd.concat([
        pd.DataFrame({'is_london': is_london, 'district': district}), postcode_df
    ], axis=1)

    if clean:
        # Actual cleaning
        print('Cleaning postcodes in ' + str_series.name)
        # Delete unrecognized districts
        del_pattern = postcode_df.district.isna()
        if del_pattern.sum() > 0:
            print('Deleting {} districts not recognized'.format(del_pattern.sum()))
            print(str_series[del_pattern].value_counts())
            postcode_df = postcode_df[~del_pattern]
            str_series = str_series[~del_pattern]

        # Delete districts outside London
        del_pattern = ~postcode_df.is_london
        if del_pattern.sum() > 0:
            print('Deleting {} districts outside London, listing districts with freq >= 100'.format(del_pattern.sum()))
            print_series = postcode_df.district[del_pattern].value_counts()
            print(print_series[print_series >= 100])
            postcode_df = postcode_df[~del_pattern]
            postcode_df.drop(columns='is_london', inplace=True)
            str_series = str_series[~del_pattern]

        # Delete unrecognized London outcode
        del_pattern = postcode_df.outcode.isna()
        if del_pattern.sum() > 0:
            print('Deleting {} unrecognized London outcodes'.format(del_pattern.sum()))
            print(str_series[del_pattern].value_counts().head(20))
            postcode_df = postcode_df[~del_pattern]

    return postcode_df


if __name__ == "__main__":
    df = pd.read_feather(utils.path_to('data', 'raw', 'jobs.feather'))
    clean_dataframe_p1(df.head(100))
