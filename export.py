import geopandas as gpd


def export_shp(shp_gdf, shp_name):
    # Xuất shapfile
    shp_gdf.to_file(shp_name)
