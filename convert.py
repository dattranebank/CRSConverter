import geopandas as gpd


def from_1984_to_1948_48n(shp_gdf):
    # Chuyển đổi hệ tọa độ từ WGS 1984 (EPSG:4326) sang WGS 1984 UTM Zone 48N (EPSG:32648)
    gdf_1984_48n = shp_gdf.to_crs(epsg=32648)
    print(f'CRS sau khi chuyển đổi: {gdf_1984_48n.crs}')
    return gdf_1984_48n
