import geopandas as gpd
import os

# Đường dẫn tới file Shapefile
shp_path = "D:\\VQG_TramChim\\01_base_maps_raw_data\\water.shp"

# Kiểm tra xem file Shapefile có tồn tại không
if os.path.exists(shp_path):
    try:
        # Đọc Shapefile (bao gồm .shp, .shx, .dbf, .prj)
        shapefile = gpd.read_file(shp_path)

        # Giữ cột
        columns_to_keep = ["ID","geometry"]  # Chọn những cột muốn giữ
        shapefile = shapefile[columns_to_keep]

        # Đường dẫn để lưu file GeoJSON
        geojson_path = "D:\\VQG_TramChim\\04_base_maps_WGS1984_GeoJSON\\water.geojson"

        # Lưu thành GeoJSON
        shapefile.to_file(geojson_path, driver="GeoJSON")
        print(f"Chuyển đổi thành công! File GeoJSON được lưu tại: {geojson_path}")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi chuyển đổi: {e}")
else:
    print(f"File Shapefile không tồn tại tại đường dẫn: {shp_path}")