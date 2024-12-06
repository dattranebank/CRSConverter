import fiona
from pyproj import CRS, Transformer
from shapely.geometry import Point, LineString, Polygon, shape, mapping

# Định nghĩa CRS đầu vào (WGS 1984 48N)
wgs84_48n = CRS.from_epsg(4326)  # WGS 1984
# Định nghĩa CRS đầu ra (VN2000 48N với 7 tham số)
vn2000_48n = CRS.from_proj4(
    f"+proj=utm +zone=48 +datum=WGS84 +towgs84=191.904,39.303,111.451,0.009288,0.019754,0.004273,-0.252906 +units=m +no_defs"
)

# Tạo Transformer để chuyển đổi CRS
transformer = Transformer.from_crs(wgs84_48n, vn2000_48n, always_xy=True)

# Hàm chuyển đổi hình học
def transform_geometry(geom):
    if geom.is_empty:
        return geom
    # Chuyển đổi các loại hình học (Point, LineString, Polygon)
    elif isinstance(geom, Point):
        x, y = transformer.transform(geom.x, geom.y)
        return Point(x, y)
    elif isinstance(geom, LineString):
        return LineString([transformer.transform(x, y) for x, y in geom.coords])
    elif isinstance(geom, Polygon):
        exterior = LineString([transformer.transform(x, y) for x, y in geom.exterior.coords])
        interiors = [LineString([transformer.transform(x, y) for x, y in interior.coords]) for interior in geom.interiors]
        return Polygon(exterior, interiors)
    else:
        return geom

# Đọc shapefile với Fiona
input_shp = "D:\\VQG_TramChim\\02_base_maps_WGS1984_48N\\ABM_WGS_1984_48N\\Vietnam_1984_48n.shp"
with fiona.open(input_shp, 'r') as source:
    schema = source.schema
    crs = source.crs

    # Ghi shapefile mới với CRS đã chuyển đổi
    output_shp = "D:\\VQG_TramChim\\output_vn2000_48n.shp"
    with fiona.open(output_shp, 'w', driver=source.driver, crs=vn2000_48n.to_wkt(), schema=schema) as sink:
        for feature in source:
            geom = shape(feature['geometry'])
            transformed_geom = transform_geometry(geom)
            feature['geometry'] = mapping(transformed_geom)  # Chuyển đổi geometry thành dict hợp lệ
            sink.write(feature)
