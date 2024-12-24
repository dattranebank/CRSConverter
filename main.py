import geopandas as gpd

from convert import from_1984_to_1948_48n
from read import *
from convert import *
from calculate import *
from export import *


def main():
    # Đường dẫn shapefile
    shp_path = "D:\\VQG_TramChim\\01_base_maps_raw_data\\DongThap.shp"
    # Đọc shapefile
    shp_gdf = read_shp(shp_path)

    # Chuyển đổi WGS 1984 sang WGS 1984 UTM Zone 48N
    gdf_1984_48n = from_1984_to_1948_48n(shp_gdf)
    # Chuyển đổi WGS 1984 48N sang VN2000 48N
    # gdf_vn2000_48n = from_1948_48n_to_vn2000_48n(gdf_1984_48n)

    # Tính diện tích
    gdf_1984_48n = calculate_area(gdf_1984_48n)
    # gdf_vn2000_48n = calculate_area(gdf_vn2000_48n)
    # Xuất shapefile
    export_shp(gdf_1984_48n, "DongThap_1984_48n.shp")
    # export_shp(gdf_vn2000_48n, "Vietnam_2000_48n.shp")


if __name__ == "__main__":
    main()
