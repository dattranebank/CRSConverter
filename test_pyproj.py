import geopandas as gpd
from pyproj import CRS, Transformer
from shapely.geometry import Point, LineString, Polygon, MultiPolygon, MultiLineString

# Đọc shapefile đầu vào (WGS 1984 48N)
input_shp = "D:\\VQG_TramChim\\02_base_maps_WGS1984_48N\\ABM_WGS_1984_48N\\Vietnam_1984_48n.shp"
data = gpd.read_file(input_shp)

# Tham số 7 yếu tố
delta_x, delta_y, delta_z = 191.904, 39.303, 111.451
rx = 0.009288 * (3.141592653589793 / 648000)  # Đơn vị: rad
ry = 0.019754 * (3.141592653589793 / 648000)  # Đơn vị: rad
rz = 0.004273 * (3.141592653589793 / 648000)  # Đơn vị: rad
s = -0.252906 / 1e6  # Đơn vị: scale (ppm -> hệ số)

# Định nghĩa CRS đầu vào (WGS 1984 48N)
wgs84_48n = CRS.from_proj4("+proj=utm +zone=48 +datum=WGS84 +units=m +no_defs")

# Định nghĩa CRS đầu ra (VN2000 48N với 7 tham số)
vn2000_48n = CRS.from_proj4(
    f"+proj=utm +zone=48 +datum=WGS84 +towgs84={delta_x},{delta_y},{delta_z},{rx},{ry},{rz},{s} +units=m +no_defs"
)

# Đặt tên cho CRS VN_2000_UTM_Zone_48N
vn2000_48n = vn2000_48n.to_wkt("WKT2")  # Sử dụng WKT2 thay vì WKT1 để ghi shapefile

# Tạo Transformer để chuyển đổi
transformer = Transformer.from_crs(wgs84_48n, vn2000_48n, always_xy=True)

# Hàm chuyển đổi hình học
def transform_geometry(geom):
    if geom.is_empty:
        return geom
    elif isinstance(geom, Point):
        # Chuyển đổi điểm
        x, y = transformer.transform(geom.x, geom.y)
        return Point(x, y)
    elif isinstance(geom, LineString):
        # Chuyển đổi LineString
        return LineString([transformer.transform(x, y) for x, y in geom.coords])
    elif isinstance(geom, Polygon):
        # Chuyển đổi Polygon (cả exterior và interiors)
        exterior = LineString([transformer.transform(x, y) for x, y in geom.exterior.coords])
        interiors = [
            LineString([transformer.transform(x, y) for x, y in interior.coords])
            for interior in geom.interiors
        ]
        return Polygon(exterior, interiors)
    elif isinstance(geom, (MultiPolygon, MultiLineString)):
        # Chuyển đổi các phần tử của MultiPolygon hoặc MultiLineString
        return geom.__class__([transform_geometry(part) for part in geom.geoms])
    else:
        # GeometryCollection hoặc các loại khác
        return geom

# Áp dụng chuyển đổi
data["geometry"] = data["geometry"].apply(transform_geometry)

# Gán CRS mới cho shapefile và ghi đè CRS cũ
data.set_crs(vn2000_48n, allow_override=True, inplace=True)

# Lưu shapefile mới
output_shp = "D:\\VQG_TramChim\\output_vn2000_48n.shp"
data.to_file(output_shp)
