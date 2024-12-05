import geopandas as gpd


def calculate_area(shp_gdf):
    # Tính diện tích cho mỗi đối tượng trong GeoDataFrame
    shp_gdf['area km2'] = shp_gdf.geometry.area

    # In ra diện tích của một số đối tượng
    print(shp_gdf[['geometry', 'area km2']].head())
    return shp_gdf


