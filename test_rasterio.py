import fiona
from shapely.geometry import shape, mapping
from rasterio.warp import transform_geom
from pyproj import CRS, Transformer

# Định nghĩa CRS đầu vào và đầu ra (VN2000 48N và WGS84)
wgs84 = CRS.from_epsg(32648)  # WGS 1984
vn2000_48n = CRS.from_proj4(
    f"+proj=utm +zone=48 +datum=WGS84 +towgs84=191.904,39.303,111.451,0.009288,0.019754,0.004273,-0.252906 +units=m +no_defs"
)

# Đọc Shapefile gốc và chuyển đổi CRS
input_shp = "D:\\VQG_TramChim\\02_base_maps_WGS1984_48N\\ABM_WGS_1984_48N\\Vietnam_1984_48n.shp"
output_shp = "D:\\VQG_TramChim\\output_vn2000_48n.shp"

with fiona.open(input_shp, 'r') as source:
    # Lấy schema và CRS hiện tại của Shapefile
    schema = source.schema
    crs = source.crs

    # Kiểm tra nếu CRS của Shapefile không phải WGS 84 (EPSG:4326), tiến hành chuyển đổi
    if crs != wgs84.to_wkt():
        print(f"CRS của Shapefile hiện tại là: {crs}")
    else:
        print(f"CRS của Shapefile là WGS 84 (EPSG:4326), bắt đầu chuyển đổi...")

    # Mở Shapefile mới với CRS VN2000 48N
    with fiona.open(output_shp, 'w', driver=source.driver, crs=vn2000_48n.to_wkt(), schema=schema) as sink:
        for feature in source:
            # Chuyển đổi geometry sang dạng shapely geometry
            geom = shape(feature['geometry'])

            # Chuyển đổi CRS của geometry từ WGS 84 sang VN2000 48N sử dụng rasterio
            transformed_geom = transform_geom(wgs84, vn2000_48n, feature['geometry'])

            # Cập nhật geometry của feature
            feature['geometry'] = mapping(transformed_geom)

            # Ghi feature vào Shapefile mới
            sink.write(feature)
