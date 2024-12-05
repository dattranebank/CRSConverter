import geopandas as gpd


def export_shp(shp_gdf):
    # Xuất shapfile
    shp_gdf.to_file("output_shapefile_utm48n.shp")
