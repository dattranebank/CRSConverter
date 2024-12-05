import geopandas as gpd
from calculate import *


def read_shp(shp_path):
    shp_gdf = gpd.read_file(shp_path)

    # In ra CRS (Coordinate Reference System) hiện tại của shapefile
    print(f'CRS hiện tại: {shp_gdf.crs}')
    return shp_gdf
