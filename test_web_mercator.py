import geopandas as gpd

# Đường dẫn tệp shapefile đầu vào
input_shp = "D:\\VQG_TramChim\\02_base_maps_WGS1984_48N\\Vietnam_1984_48n.shp"
# Đường dẫn tệp shapefile đầu ra
output_shp = "Vietnam_1984_Web_Mercator.shp"

# Mở tệp shapefile
gdf = gpd.read_file(input_shp)

# Xác định hệ tọa độ ban đầu (WGS 1984 UTM Zone 48N)
gdf = gdf.set_crs(epsg=32648)  # EPSG:32648 là mã của WGS 1984 UTM Zone 48N

# Chuyển đổi sang hệ tọa độ Web Mercator (EPSG:3857)
gdf = gdf.to_crs(epsg=3857)

# Lưu tệp shapefile sau khi chuyển đổi
gdf.to_file(output_shp)

print("Chuyển đổi hệ tọa độ hoàn tất!")
