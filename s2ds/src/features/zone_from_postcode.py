import pandas as pd
import re
import warnings
import utils


def read_postcode_csv(csv_file):
    csv_table = pd.read_csv(utils.path_to('src', 'features', csv_file))

    zone_lookup = dict(zip(csv_table['postcode'], csv_table['zone']))

    return zone_lookup


ZONE_LOOKUP = read_postcode_csv("postcode_district_list_with_zones.csv")


def zone_from_postcode(postcode):

    re_division = re.compile('^[EWNS][ECW]?[0-9]{1,2}')
    division = re.match(re_division, postcode).group(0)
    key = division

    if key in ZONE_LOOKUP:
        return ZONE_LOOKUP[key]
    else:
        warnings.warn("Missing key " + key, stacklevel=2)
        return 'NA'
