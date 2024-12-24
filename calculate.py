import geopandas as gpd


def calculate_area(shp_gdf):
    # Tính diện tích cho mỗi đối tượng trong GeoDataFrame
    shp_gdf['Area km2'] = (shp_gdf.geometry.area/1_000_000).round(3)

    # In ra diện tích của một số đối tượng
    print(shp_gdf[['geometry', 'Area km2']].head())
    return shp_gdf


