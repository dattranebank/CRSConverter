from functools import partial

import geopandas as gpd
import pyproj
from pyproj import CRS, Transformer, transform


def from_1984_to_1948_48n(shp_gdf):
    # Chuyển đổi hệ tọa độ từ WGS 1984 (EPSG:4326) sang WGS 1984 UTM Zone 48N (EPSG:32648)
    gdf_1984_48n = shp_gdf.to_crs(epsg=32648)
    print(f'CRS sau khi chuyển đổi: {gdf_1984_48n.crs}')
    return gdf_1984_48n


def from_1948_48n_to_vn2000_48n(shp_gdf):
    # Định nghĩa CRS đầu vào (WGS 1984 48N) và đầu ra (VN2000 48N với 7 tham số)
    wgs84_48n = CRS.from_proj4("+proj=utm +zone=48 +datum=WGS84 +units=m +no_defs")
    vn2000_48n = CRS.from_proj4(
        "+proj=utm +zone=48 +datum=WGS84 +towgs84=delta_x,delta_y,delta_z,rx,ry,rz,s +units=m +no_defs"
    )
    # Các tham số chuyển đổi 7 tham số (có thể cần chuyển đổi rx, ry, rz sang radian)
    delta_x = 191.90441429  # ΔX
    delta_y = 39.30318279  # ΔY
    delta_z = 111.45032835  # ΔZ
    rx = 0.00928836 / 3600 * (3.141592653589793 / 180)  # Rx chuyển sang radian
    ry = -0.01975479 / 3600 * (3.141592653589793 / 180)  # Ry chuyển sang radian
    rz = 0.00427372 / 3600 * (3.141592653589793 / 180)  # Rz chuyển sang radian
    s = -0.252906278  # S (tỷ lệ)

    # Pipeline với `helmert`
    transformer = pyproj.Transformer.from_pipeline(f"""
    +proj=pipeline
    +step +proj=latlong +datum=WGS84
    +step +proj=utm +zone=48 +datum=WGS84
    +step +proj=helmert +x={delta_x} +y={delta_y} +z={delta_z} +rx={rx} +ry={ry} +rz={rz} +s={s} +convention=coordinate_frame
    +step +proj=utm +zone=48 +datum=VN2000
    """)

    # Hàm chuyển đổi hình học
    project = partial(transformer.transform)

    # Áp dụng chuyển đổi
    shp_gdf['geometry'] = shp_gdf['geometry'].apply(lambda geom: transform(project, geom))

    return shp_gdf
