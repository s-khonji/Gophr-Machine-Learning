import pandas as pd
import numpy as np
from datetime import datetime
import features

def cyclic_from_datetime(dt_object, cycle):
    """ transform datetime object to cyclic arc and return cartesian cordinates
    [Return] Tuple of sin and cos variable
    """
    return arc_cordinates(cycle.seconds(dt_object), cycle.duration)
    # return pd.DataFrame(list(zip(*polar_cordinates(cycle.seconds(dt_object), cycle.duration))))


def arc_cordinates(arc, circumference):
    """  transform arc in radians to cartesian coordinates
    [Return] Tuple cartesian cordinates, y (sin) and x (cos)
    """
    y = np.sin(arc * (2. * np.pi / circumference))
    x = np.cos(arc * (2. * np.pi / circumference))

    return y, x


if __name__ == "__main__":
    today = pd.Series(datetime.now())

    day_sin, day_cos = cyclic_from_datetime(today, features.CYCLE_DAY)
    print('Second a day:  {}'.format([day_sin.values[0], day_cos.values[0]]))

    week_sin, week_cos = cyclic_from_datetime(today, features.CYCLE_WEEK)
    print('Second a week: {}'.format([week_sin.values[0], week_cos.values[0]]))

    year_sin, year_cos = cyclic_from_datetime(today, features.CYCLE_YEAR)
    print('Second a year: {}'.format([year_sin.values[0], year_cos.values[0]]))
