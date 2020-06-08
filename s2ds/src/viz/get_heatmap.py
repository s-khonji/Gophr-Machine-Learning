import pickle
import utils
import os
import geopandas as gpd
from shapely.geometry import Point


def get_postcode_heatmap(df, target_str,
                         postcode='pickup_postcode_outer',
                         shape_file_name='london_shape.bin',
                         shape_file_path=utils.path_to('src', 'viz')):
    """
    """
    # load shape files
    london_shp = _load_shape_file(shape_file_name, shape_file_path)

    # Average data within the postcode
    avg_target = df.groupby(postcode)[target_str].mean().round(1)

    # merge on postcode index
    heatmap_gdf = london_shp.merge(avg_target, left_index=True, right_index=True, how='left')

    return heatmap_gdf


def get_point_heatmap(df, location_lng, location_lat,
                      shape_file_name='london_shape.bin',
                      shape_file_path=utils.path_to('src', 'viz')):
    """
    """

    # load shape files
    london_shp = _load_shape_file(shape_file_name, shape_file_path)

    # data points to gdp
    gdf = gpd.GeoDataFrame(df, crs={'init': 'epsg:4326'},
                           geometry=[Point(xy) for xy in zip(location_lng, location_lat)])

    return gdf, london_shp


def _load_shape_file(shape_file_name, shape_file_path):
    """
    """
    return pickle.load(file=open(os.path.join(shape_file_path, shape_file_name), 'rb')).to_crs("EPSG:4326")
