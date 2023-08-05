from tests.data.coordinates import (
    point_coordinates,
    linestring_coordinates,
    polygon_coordinates,
    multipoint_coordinates,
    multilinestring_coordinates,
    multipolygon_coordinates,
    point_coordinates_3d,
    linestring_coordinates_3d,
    polygon_coordinates_3d,
    multipoint_coordinates_3d,
    multilinestring_coordinates_3d,
    multipolygon_coordinates_3d,
)

# FORMAT : geojson like

POINT = {"type": "Point", "coordinates": point_coordinates}
POINT_EMPTY = {"type": "Point", "coordinates": []}
MULTIPOINT = {"type": "MultiPoint", "coordinates": multipoint_coordinates}
MULTIPOINT_EMPTY = {"type": "MultiPoint", "coordinates": []}
LINESTRING = {"type": "LineString", "coordinates": linestring_coordinates}
LINESTRING_EMPTY = {"type": "LineString", "coordinates": []}

LINESTRING_TEST_POINT_ON_LINESTRING = {"type": "LineString", "coordinates": [[-10, -10], [-10, 10], [10, 10]]}
LINESTRING_TEST_POINT_ON_LINESTRING_REVERSE = {"type": "LineString", "coordinates": [[10, 10], [-10, 10], [-10, -10]]}

MULTILINESTRING = {
    "type": "MultiLineString",
    "coordinates": multilinestring_coordinates,
}
MULTILINESTRING_EMPTY = {"type": "MultiLineString", "coordinates": []}
POLYGON = {"type": "Polygon", "coordinates": polygon_coordinates}
POLYGON_EMPTY = {"type": "Polygon", "coordinates": []}
MULTIPOLYGON = {"type": "MultiPolygon", "coordinates": multipolygon_coordinates}
MULTIPOLYGON_EMPTY = {"type": "MultiPolygon", "coordinates": []}
GEOMETRYCOLLECTION = {
    "type": "GeometryCollection",
    "geometries": [
        {"type": "Point", "coordinates": [-115.81, 37.24]},
        {"type": "LineString", "coordinates": [[8.919, 44.4074], [8.923, 44.4075]]},
        {
            "type": "Polygon",
            "coordinates": [
                [[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]],
                [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]],
            ],
        },
        {
            "type": "MultiPoint",
            "coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]],
        },
        {
            "type": "MultiLineString",
            "coordinates": [
                [[3.75, 9.25], [-130.95, 1.52]],
                [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]],
            ],
        },
        {
            "type": "MultiPolygon",
            "coordinates": [
                [[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]],
                [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]],
            ],
        },
    ],
}
GEOMETRYCOLLECTION_EMPTY = {"type": "GeometryCollection", "geometries": []}
GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES = {
    "type": "GeometryCollection",
    "geometries": [
        {"type": "Point", "coordinates": []},
        {"type": "LineString", "coordinates": [[8.919, 44.4074], [8.923, 44.4075]]},
        {
            "type": "Polygon",
            "coordinates": [
                [[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]],
                [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]],
            ],
        },
        {"type": "MultiPoint", "coordinates": []},
        {
            "type": "MultiLineString",
            "coordinates": [
                [[3.75, 9.25], [-130.95, 1.52]],
                [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]],
            ],
        },
        {"type": "MultiPolygon", "coordinates": []},
    ],
}

# 3D
POINT_3D = {"type": "Point25D", "coordinates": point_coordinates_3d}
LINESTRING_3D = {"type": "LineString25D", "coordinates": linestring_coordinates_3d}
POLYGON_3D = {"type": "Polygon25D", "coordinates": polygon_coordinates_3d}
MULTIPOINT_3D = {"type": "MultiPoint25D", "coordinates": multipoint_coordinates_3d}
MULTILINESTRING_3D = {
    "type": "MultiLineString25D",
    "coordinates": multilinestring_coordinates_3d,
}
MULTIPOLYGON_3D = {
    "type": "MultiPolygon25D",
    "coordinates": multipolygon_coordinates_3d,
}
GEOMETRYCOLLECTION_3D = {
    "type": "GeometryCollection",
    "geometries": [
        POINT_3D,
        LINESTRING_3D,
        POLYGON_3D,
        MULTIPOINT_3D,
        MULTILINESTRING_3D,
        MULTIPOLYGON_3D,
    ],
}


# FORMAT : geoformat geojson like + bbox
POINT_WITH_BBOX = {
    "type": "Point",
    "coordinates": point_coordinates,
    "bbox": (-115.81, 37.24, -115.81, 37.24),
}
MULTIPOINT_WITH_BBOX = {
    "type": "MultiPoint",
    "coordinates": multipoint_coordinates,
    "bbox": (-157.97, 19.61, -155.52, 21.46),
}
LINESTRING_WITH_BBOX = {
    "type": "LineString",
    "coordinates": linestring_coordinates,
    "bbox": (8.919, 44.4074, 8.923, 44.4075),
}
MULTILINESTRING_WITH_BBOX = {
    "type": "MultiLineString",
    "coordinates": multilinestring_coordinates,
    "bbox": (-130.95, -34.25, 23.15, 77.95),
}
POLYGON_WITH_BBOX = {
    "type": "Polygon",
    "coordinates": polygon_coordinates,
    "bbox": (-120.43, -20.28, 23.194, 57.322),
}
MULTIPOLYGON_WITH_BBOX = {
    "type": "MultiPolygon",
    "coordinates": multipolygon_coordinates,
    "bbox": (-130.91, -34.29, 35.12, 77.91),
}
GEOMETRYCOLLECTION_WITH_BBOX = {
    "type": "GeometryCollection",
    "geometries": [
        {
            "type": "Point",
            "coordinates": [-115.81, 37.24],
            "bbox": (-115.81, 37.24, -115.81, 37.24),
        },
        {
            "type": "LineString",
            "coordinates": [[8.919, 44.4074], [8.923, 44.4075]],
            "bbox": (8.919, 44.4074, 8.923, 44.4075),
        },
        {
            "type": "Polygon",
            "coordinates": [
                [[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]],
                [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]],
            ],
            "bbox": (-120.43, -20.28, 23.194, 57.322),
        },
        {
            "type": "MultiPoint",
            "coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]],
            "bbox": (-157.97, 19.61, -155.52, 21.46),
        },
        {
            "type": "MultiLineString",
            "coordinates": [
                [[3.75, 9.25], [-130.95, 1.52]],
                [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]],
            ],
            "bbox": (-130.95, -34.25, 23.15, 77.95),
        },
        {
            "type": "MultiPolygon",
            "coordinates": [
                [[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]],
                [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]],
            ],
            "bbox": (-130.91, -34.29, 35.12, 77.91),
        },
    ],
    "bbox": (-157.97, -34.29, 35.12, 77.95),
}
GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WITH_BBOX = {
    "type": "GeometryCollection",
    "geometries": [
        {"type": "Point", "coordinates": []},
        {
            "type": "LineString",
            "coordinates": [[8.919, 44.4074], [8.923, 44.4075]],
            "bbox": (8.919, 44.4074, 8.923, 44.4075),
        },
        {
            "type": "Polygon",
            "coordinates": [
                [[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]],
                [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]],
            ],
            "bbox": (-120.43, -20.28, 23.194, 57.322),
        },
        {"type": "MultiPoint", "coordinates": []},
        {
            "type": "MultiLineString",
            "coordinates": [
                [[3.75, 9.25], [-130.95, 1.52]],
                [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]],
            ],
            "bbox": (-130.95, -34.25, 23.15, 77.95),
        },
        {"type": "MultiPolygon", "coordinates": []},
    ],
    "bbox": (-130.95, -34.25, 23.194, 77.95),
}

# format : WKB with big endian
POINT_WKB_BIG_ENDIAN = (
    b"\x00\x00\x00\x00\x01\xc0\\\xf3\xd7\n=p\xa4@B\x9e\xb8Q\xeb\x85\x1f"
)
POINT_EMPTY_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x01\x7f\xf8\x00\x00\x00\x00\x00\x00\x7f\xf8\x00\x00\x00\x00\x00\x00"
LINESTRING_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x02\x00\x00\x00\x02@!\xd6\x87+\x02\x0cJ@F4%\xae\xe61\xf9@!\xd8\x93t\xbcj\x7f@F4(\xf5\xc2\x8f\\"
LINESTRING_EMPTY_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x02\x00\x00\x00\x00"
POLYGON_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x04@\x03\n=p\xa3\xd7\n@L\xa97K\xc6\xa7\xf0@71\xa9\xfb\xe7l\x8b\xc04G\xae\x14z\xe1H\xc0^\x1b\x85\x1e\xb8Q\xec@3&fffff@\x03\n=p\xa3\xd7\n@L\xa97K\xc6\xa7\xf0\x00\x00\x00\x04\xc0\x14\xd7\n=p\xa3\xd7@7\x82\x8f\\(\xf5\xc3@.k\x85\x1e\xb8Q\xec\xc0%\x9e\xb8Q\xeb\x85\x1f\xc04\x82\x8f\\(\xf5\xc3?\xf8(\xf5\xc2\x8f\\)\xc0\x14\xd7\n=p\xa3\xd7@7\x82\x8f\\(\xf5\xc3"
POLYGON_EMPTY_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x03\x00\x00\x00\x00"
MULTIPOINT_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x00\x01\xc0cp\xa3\xd7\n=q@3\x9c(\xf5\xc2\x8f\\\x00\x00\x00\x00\x01\xc0c\x87\n=p\xa3\xd7@4\xbdp\xa3\xd7\n=\x00\x00\x00\x00\x01\xc0c\xbf\n=p\xa3\xd7@5u\xc2\x8f\\(\xf6"
MULTIPOINT_EMPTY_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x04\x00\x00\x00\x00"
MULTILINESTRING_WKB_BIG_ENDIAN = b'\x00\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x00\x02\x00\x00\x00\x02@\x0e\x00\x00\x00\x00\x00\x00@"\x80\x00\x00\x00\x00\x00\xc0`^fffff?\xf8Q\xeb\x85\x1e\xb8R\x00\x00\x00\x00\x02\x00\x00\x00\x03@7&fffff\xc0A \x00\x00\x00\x00\x00\xbf\xf5\x99\x99\x99\x99\x99\x9a\xc0\x12\x99\x99\x99\x99\x99\x9a@\x0b\x99\x99\x99\x99\x99\x9a@S|\xcc\xcc\xcc\xcc\xcd'
MULTILINESTRING_EMPTY_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x05\x00\x00\x00\x00"
MULTIPOLYGON_WKB_BIG_ENDIAN = b'\x00\x00\x00\x00\x06\x00\x00\x00\x02\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x04@\x0e=p\xa3\xd7\n=@"\x8f\\(\xf5\xc2\x8f\xc0`]\x1e\xb8Q\xeb\x85?\xf8Q\xeb\x85\x1e\xb8R@A\x8f\\(\xf5\xc2\x8f@R\x0e\xf9\xdb"\xd0\xe5@\x0e=p\xa3\xd7\n=@"\x8f\\(\xf5\xc2\x8f\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x04@7.\x14z\xe1G\xae\xc0A%\x1e\xb8Q\xeb\x85\xbf\xf4\xf5\xc2\x8f\\(\xf6\xc0\x12p\xa3\xd7\n=q@\x0bG\xae\x14z\xe1H@Sz=p\xa3\xd7\n@7.\x14z\xe1G\xae\xc0A%\x1e\xb8Q\xeb\x85'
MULTIPOLYGON_EMPTY_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x06\x00\x00\x00\x00"
GEOMETRYCOLLECTION_WKB_BIG_ENDIAN = b'\x00\x00\x00\x00\x07\x00\x00\x00\x06\x00\x00\x00\x00\x01\xc0\\\xf3\xd7\n=p\xa4@B\x9e\xb8Q\xeb\x85\x1f\x00\x00\x00\x00\x02\x00\x00\x00\x02@!\xd6\x87+\x02\x0cJ@F4%\xae\xe61\xf9@!\xd8\x93t\xbcj\x7f@F4(\xf5\xc2\x8f\\\x00\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x04@\x03\n=p\xa3\xd7\n@L\xa97K\xc6\xa7\xf0@71\xa9\xfb\xe7l\x8b\xc04G\xae\x14z\xe1H\xc0^\x1b\x85\x1e\xb8Q\xec@3&fffff@\x03\n=p\xa3\xd7\n@L\xa97K\xc6\xa7\xf0\x00\x00\x00\x04\xc0\x14\xd7\n=p\xa3\xd7@7\x82\x8f\\(\xf5\xc3@.k\x85\x1e\xb8Q\xec\xc0%\x9e\xb8Q\xeb\x85\x1f\xc04\x82\x8f\\(\xf5\xc3?\xf8(\xf5\xc2\x8f\\)\xc0\x14\xd7\n=p\xa3\xd7@7\x82\x8f\\(\xf5\xc3\x00\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x00\x01\xc0cp\xa3\xd7\n=q@3\x9c(\xf5\xc2\x8f\\\x00\x00\x00\x00\x01\xc0c\x87\n=p\xa3\xd7@4\xbdp\xa3\xd7\n=\x00\x00\x00\x00\x01\xc0c\xbf\n=p\xa3\xd7@5u\xc2\x8f\\(\xf6\x00\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x00\x02\x00\x00\x00\x02@\x0e\x00\x00\x00\x00\x00\x00@"\x80\x00\x00\x00\x00\x00\xc0`^fffff?\xf8Q\xeb\x85\x1e\xb8R\x00\x00\x00\x00\x02\x00\x00\x00\x03@7&fffff\xc0A \x00\x00\x00\x00\x00\xbf\xf5\x99\x99\x99\x99\x99\x9a\xc0\x12\x99\x99\x99\x99\x99\x9a@\x0b\x99\x99\x99\x99\x99\x9a@S|\xcc\xcc\xcc\xcc\xcd\x00\x00\x00\x00\x06\x00\x00\x00\x02\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x04@\x0e=p\xa3\xd7\n=@"\x8f\\(\xf5\xc2\x8f\xc0`]\x1e\xb8Q\xeb\x85?\xf8Q\xeb\x85\x1e\xb8R@A\x8f\\(\xf5\xc2\x8f@R\x0e\xf9\xdb"\xd0\xe5@\x0e=p\xa3\xd7\n=@"\x8f\\(\xf5\xc2\x8f\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x04@7.\x14z\xe1G\xae\xc0A%\x1e\xb8Q\xeb\x85\xbf\xf4\xf5\xc2\x8f\\(\xf6\xc0\x12p\xa3\xd7\n=q@\x0bG\xae\x14z\xe1H@Sz=p\xa3\xd7\n@7.\x14z\xe1G\xae\xc0A%\x1e\xb8Q\xeb\x85'
GEOMETRYCOLLECTION_EMPTY_WKB_BIG_ENDIAN = b"\x00\x00\x00\x00\x07\x00\x00\x00\x00"
GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_BIG_ENDIAN = b'\x00\x00\x00\x00\x07\x00\x00\x00\x06\x00\x00\x00\x00\x01\x7f\xf8\x00\x00\x00\x00\x00\x00\x7f\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02@!\xd6\x87+\x02\x0cJ@F4%\xae\xe61\xf9@!\xd8\x93t\xbcj\x7f@F4(\xf5\xc2\x8f\\\x00\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x04@\x03\n=p\xa3\xd7\n@L\xa97K\xc6\xa7\xf0@71\xa9\xfb\xe7l\x8b\xc04G\xae\x14z\xe1H\xc0^\x1b\x85\x1e\xb8Q\xec@3&fffff@\x03\n=p\xa3\xd7\n@L\xa97K\xc6\xa7\xf0\x00\x00\x00\x04\xc0\x14\xd7\n=p\xa3\xd7@7\x82\x8f\\(\xf5\xc3@.k\x85\x1e\xb8Q\xec\xc0%\x9e\xb8Q\xeb\x85\x1f\xc04\x82\x8f\\(\xf5\xc3?\xf8(\xf5\xc2\x8f\\)\xc0\x14\xd7\n=p\xa3\xd7@7\x82\x8f\\(\xf5\xc3\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x00\x02\x00\x00\x00\x02@\x0e\x00\x00\x00\x00\x00\x00@"\x80\x00\x00\x00\x00\x00\xc0`^fffff?\xf8Q\xeb\x85\x1e\xb8R\x00\x00\x00\x00\x02\x00\x00\x00\x03@7&fffff\xc0A \x00\x00\x00\x00\x00\xbf\xf5\x99\x99\x99\x99\x99\x9a\xc0\x12\x99\x99\x99\x99\x99\x9a@\x0b\x99\x99\x99\x99\x99\x9a@S|\xcc\xcc\xcc\xcc\xcd\x00\x00\x00\x00\x06\x00\x00\x00\x00'

# format : WKB with little endian
POINT_WKB_LITTLE_ENDIAN = (
    b"\x01\x01\x00\x00\x00\xa4p=\n\xd7\xf3\\\xc0\x1f\x85\xebQ\xb8\x9eB@"
)
POINT_EMPTY_WKB_LITTLE_ENDIAN = b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f"
LINESTRING_WKB_LITTLE_ENDIAN = b"\x01\x02\x00\x00\x00\x02\x00\x00\x00J\x0c\x02+\x87\xd6!@\xf91\xe6\xae%4F@\x7fj\xbct\x93\xd8!@\\\x8f\xc2\xf5(4F@"
LINESTRING_EMPTY_WKB_LITTLE_ENDIAN = b"\x01\x02\x00\x00\x00\x00\x00\x00\x00"
POLYGON_WKB_LITTLE_ENDIAN = b"\x01\x03\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\n\xd7\xa3p=\n\x03@\xf0\xa7\xc6K7\xa9L@\x8bl\xe7\xfb\xa917@H\xe1z\x14\xaeG4\xc0\xecQ\xb8\x1e\x85\x1b^\xc0fffff&3@\n\xd7\xa3p=\n\x03@\xf0\xa7\xc6K7\xa9L@\x04\x00\x00\x00\xd7\xa3p=\n\xd7\x14\xc0\xc3\xf5(\\\x8f\x827@\xecQ\xb8\x1e\x85k.@\x1f\x85\xebQ\xb8\x9e%\xc0\xc3\xf5(\\\x8f\x824\xc0)\\\x8f\xc2\xf5(\xf8?\xd7\xa3p=\n\xd7\x14\xc0\xc3\xf5(\\\x8f\x827@"
POLYGON_EMPTY_WKB_LITTLE_ENDIAN = b"\x01\x03\x00\x00\x00\x00\x00\x00\x00"
MULTIPOINT_WKB_LITTLE_ENDIAN = b"\x01\x04\x00\x00\x00\x03\x00\x00\x00\x01\x01\x00\x00\x00q=\n\xd7\xa3pc\xc0\\\x8f\xc2\xf5(\x9c3@\x01\x01\x00\x00\x00\xd7\xa3p=\n\x87c\xc0=\n\xd7\xa3p\xbd4@\x01\x01\x00\x00\x00\xd7\xa3p=\n\xbfc\xc0\xf6(\\\x8f\xc2u5@"
MULTIPOINT_EMPTY_WKB_LITTLE_ENDIAN = b"\x01\x04\x00\x00\x00\x00\x00\x00\x00"
MULTILINESTRING_WKB_LITTLE_ENDIAN = b'\x01\x05\x00\x00\x00\x02\x00\x00\x00\x01\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e@\x00\x00\x00\x00\x00\x80"@fffff^`\xc0R\xb8\x1e\x85\xebQ\xf8?\x01\x02\x00\x00\x00\x03\x00\x00\x00fffff&7@\x00\x00\x00\x00\x00 A\xc0\x9a\x99\x99\x99\x99\x99\xf5\xbf\x9a\x99\x99\x99\x99\x99\x12\xc0\x9a\x99\x99\x99\x99\x99\x0b@\xcd\xcc\xcc\xcc\xcc|S@'
MULTILINESTRING_EMPTY_WKB_LITTLE_ENDIAN = b"\x01\x05\x00\x00\x00\x00\x00\x00\x00"
MULTIPOLYGON_WKB_LITTLE_ENDIAN = b'\x01\x06\x00\x00\x00\x02\x00\x00\x00\x01\x03\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00=\n\xd7\xa3p=\x0e@\x8f\xc2\xf5(\\\x8f"@\x85\xebQ\xb8\x1e]`\xc0R\xb8\x1e\x85\xebQ\xf8?\x8f\xc2\xf5(\\\x8fA@\xe5\xd0"\xdb\xf9\x0eR@=\n\xd7\xa3p=\x0e@\x8f\xc2\xf5(\\\x8f"@\x01\x03\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\xaeG\xe1z\x14.7@\x85\xebQ\xb8\x1e%A\xc0\xf6(\\\x8f\xc2\xf5\xf4\xbfq=\n\xd7\xa3p\x12\xc0H\xe1z\x14\xaeG\x0b@\n\xd7\xa3p=zS@\xaeG\xe1z\x14.7@\x85\xebQ\xb8\x1e%A\xc0'
MULTIPOLYGON_EMPTY_WKB_LITTLE_ENDIAN = b"\x01\x06\x00\x00\x00\x00\x00\x00\x00"
GEOMETRYCOLLECTION_WKB_LITTLE_ENDIAN = b'\x01\x07\x00\x00\x00\x06\x00\x00\x00\x01\x01\x00\x00\x00\xa4p=\n\xd7\xf3\\\xc0\x1f\x85\xebQ\xb8\x9eB@\x01\x02\x00\x00\x00\x02\x00\x00\x00J\x0c\x02+\x87\xd6!@\xf91\xe6\xae%4F@\x7fj\xbct\x93\xd8!@\\\x8f\xc2\xf5(4F@\x01\x03\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\n\xd7\xa3p=\n\x03@\xf0\xa7\xc6K7\xa9L@\x8bl\xe7\xfb\xa917@H\xe1z\x14\xaeG4\xc0\xecQ\xb8\x1e\x85\x1b^\xc0fffff&3@\n\xd7\xa3p=\n\x03@\xf0\xa7\xc6K7\xa9L@\x04\x00\x00\x00\xd7\xa3p=\n\xd7\x14\xc0\xc3\xf5(\\\x8f\x827@\xecQ\xb8\x1e\x85k.@\x1f\x85\xebQ\xb8\x9e%\xc0\xc3\xf5(\\\x8f\x824\xc0)\\\x8f\xc2\xf5(\xf8?\xd7\xa3p=\n\xd7\x14\xc0\xc3\xf5(\\\x8f\x827@\x01\x04\x00\x00\x00\x03\x00\x00\x00\x01\x01\x00\x00\x00q=\n\xd7\xa3pc\xc0\\\x8f\xc2\xf5(\x9c3@\x01\x01\x00\x00\x00\xd7\xa3p=\n\x87c\xc0=\n\xd7\xa3p\xbd4@\x01\x01\x00\x00\x00\xd7\xa3p=\n\xbfc\xc0\xf6(\\\x8f\xc2u5@\x01\x05\x00\x00\x00\x02\x00\x00\x00\x01\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e@\x00\x00\x00\x00\x00\x80"@fffff^`\xc0R\xb8\x1e\x85\xebQ\xf8?\x01\x02\x00\x00\x00\x03\x00\x00\x00fffff&7@\x00\x00\x00\x00\x00 A\xc0\x9a\x99\x99\x99\x99\x99\xf5\xbf\x9a\x99\x99\x99\x99\x99\x12\xc0\x9a\x99\x99\x99\x99\x99\x0b@\xcd\xcc\xcc\xcc\xcc|S@\x01\x06\x00\x00\x00\x02\x00\x00\x00\x01\x03\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00=\n\xd7\xa3p=\x0e@\x8f\xc2\xf5(\\\x8f"@\x85\xebQ\xb8\x1e]`\xc0R\xb8\x1e\x85\xebQ\xf8?\x8f\xc2\xf5(\\\x8fA@\xe5\xd0"\xdb\xf9\x0eR@=\n\xd7\xa3p=\x0e@\x8f\xc2\xf5(\\\x8f"@\x01\x03\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\xaeG\xe1z\x14.7@\x85\xebQ\xb8\x1e%A\xc0\xf6(\\\x8f\xc2\xf5\xf4\xbfq=\n\xd7\xa3p\x12\xc0H\xe1z\x14\xaeG\x0b@\n\xd7\xa3p=zS@\xaeG\xe1z\x14.7@\x85\xebQ\xb8\x1e%A\xc0'
GEOMETRYCOLLECTION_EMPTY_WKB_LITTLE_ENDIAN = b"\x01\x07\x00\x00\x00\x00\x00\x00\x00"
GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_LITTLE_ENDIAN = b'\x01\x07\x00\x00\x00\x06\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x7f\x00\x00\x00\x00\x00\x00\xf8\x7f\x01\x02\x00\x00\x00\x02\x00\x00\x00J\x0c\x02+\x87\xd6!@\xf91\xe6\xae%4F@\x7fj\xbct\x93\xd8!@\\\x8f\xc2\xf5(4F@\x01\x03\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\n\xd7\xa3p=\n\x03@\xf0\xa7\xc6K7\xa9L@\x8bl\xe7\xfb\xa917@H\xe1z\x14\xaeG4\xc0\xecQ\xb8\x1e\x85\x1b^\xc0fffff&3@\n\xd7\xa3p=\n\x03@\xf0\xa7\xc6K7\xa9L@\x04\x00\x00\x00\xd7\xa3p=\n\xd7\x14\xc0\xc3\xf5(\\\x8f\x827@\xecQ\xb8\x1e\x85k.@\x1f\x85\xebQ\xb8\x9e%\xc0\xc3\xf5(\\\x8f\x824\xc0)\\\x8f\xc2\xf5(\xf8?\xd7\xa3p=\n\xd7\x14\xc0\xc3\xf5(\\\x8f\x827@\x01\x04\x00\x00\x00\x00\x00\x00\x00\x01\x05\x00\x00\x00\x02\x00\x00\x00\x01\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e@\x00\x00\x00\x00\x00\x80"@fffff^`\xc0R\xb8\x1e\x85\xebQ\xf8?\x01\x02\x00\x00\x00\x03\x00\x00\x00fffff&7@\x00\x00\x00\x00\x00 A\xc0\x9a\x99\x99\x99\x99\x99\xf5\xbf\x9a\x99\x99\x99\x99\x99\x12\xc0\x9a\x99\x99\x99\x99\x99\x0b@\xcd\xcc\xcc\xcc\xcc|S@\x01\x06\x00\x00\x00\x00\x00\x00\x00'

# format : WKB with varying endian in geometry
MULTIPOINT_WKB_VARYING_ENDIAN = b"\x00\x00\x00\x00\x04\x00\x00\x00\x03\x01\x01\x00\x00\x00q=\n\xd7\xa3pc\xc0\\\x8f\xc2\xf5(\x9c3@\x01\x01\x00\x00\x00\xd7\xa3p=\n\x87c\xc0=\n\xd7\xa3p\xbd4@\x01\x01\x00\x00\x00\xd7\xa3p=\n\xbfc\xc0\xf6(\\\x8f\xc2u5@"
MULTILINESTRING_WKB_VARYING_ENDIAN = b'\x00\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x00\x02\x00\x00\x00\x02@\x0e\x00\x00\x00\x00\x00\x00@"\x80\x00\x00\x00\x00\x00\xc0`^fffff?\xf8Q\xeb\x85\x1e\xb8R\x01\x02\x00\x00\x00\x03\x00\x00\x00fffff&7@\x00\x00\x00\x00\x00 A\xc0\x9a\x99\x99\x99\x99\x99\xf5\xbf\x9a\x99\x99\x99\x99\x99\x12\xc0\x9a\x99\x99\x99\x99\x99\x0b@\xcd\xcc\xcc\xcc\xcc|S@'
MULTIPOLYGON_WKB_VARYING_ENDIAN = b'\x00\x00\x00\x00\x06\x00\x00\x00\x02\x01\x03\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00=\n\xd7\xa3p=\x0e@\x8f\xc2\xf5(\\\x8f"@\x85\xebQ\xb8\x1e]`\xc0R\xb8\x1e\x85\xebQ\xf8?\x8f\xc2\xf5(\\\x8fA@\xe5\xd0"\xdb\xf9\x0eR@=\n\xd7\xa3p=\x0e@\x8f\xc2\xf5(\\\x8f"@\x01\x03\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\xaeG\xe1z\x14.7@\x85\xebQ\xb8\x1e%A\xc0\xf6(\\\x8f\xc2\xf5\xf4\xbfq=\n\xd7\xa3p\x12\xc0H\xe1z\x14\xaeG\x0b@\n\xd7\xa3p=zS@\xaeG\xe1z\x14.7@\x85\xebQ\xb8\x1e%A\xc0'
GEOMETRYCOLLECTION_WKB_VARYING_ENDIAN = b'\x00\x00\x00\x00\x07\x00\x00\x00\x06\x01\x01\x00\x00\x00\xa4p=\n\xd7\xf3\\\xc0\x1f\x85\xebQ\xb8\x9eB@\x00\x00\x00\x00\x02\x00\x00\x00\x02@!\xd6\x87+\x02\x0cJ@F4%\xae\xe61\xf9@!\xd8\x93t\xbcj\x7f@F4(\xf5\xc2\x8f\\\x01\x03\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\n\xd7\xa3p=\n\x03@\xf0\xa7\xc6K7\xa9L@\x8bl\xe7\xfb\xa917@H\xe1z\x14\xaeG4\xc0\xecQ\xb8\x1e\x85\x1b^\xc0fffff&3@\n\xd7\xa3p=\n\x03@\xf0\xa7\xc6K7\xa9L@\x04\x00\x00\x00\xd7\xa3p=\n\xd7\x14\xc0\xc3\xf5(\\\x8f\x827@\xecQ\xb8\x1e\x85k.@\x1f\x85\xebQ\xb8\x9e%\xc0\xc3\xf5(\\\x8f\x824\xc0)\\\x8f\xc2\xf5(\xf8?\xd7\xa3p=\n\xd7\x14\xc0\xc3\xf5(\\\x8f\x827@\x00\x00\x00\x00\x04\x00\x00\x00\x03\x01\x01\x00\x00\x00q=\n\xd7\xa3pc\xc0\\\x8f\xc2\xf5(\x9c3@\x01\x01\x00\x00\x00\xd7\xa3p=\n\x87c\xc0=\n\xd7\xa3p\xbd4@\x01\x01\x00\x00\x00\xd7\xa3p=\n\xbfc\xc0\xf6(\\\x8f\xc2u5@\x00\x00\x00\x00\x05\x00\x00\x00\x02\x00\x00\x00\x00\x02\x00\x00\x00\x02@\x0e\x00\x00\x00\x00\x00\x00@"\x80\x00\x00\x00\x00\x00\xc0`^fffff?\xf8Q\xeb\x85\x1e\xb8R\x01\x02\x00\x00\x00\x03\x00\x00\x00fffff&7@\x00\x00\x00\x00\x00 A\xc0\x9a\x99\x99\x99\x99\x99\xf5\xbf\x9a\x99\x99\x99\x99\x99\x12\xc0\x9a\x99\x99\x99\x99\x99\x0b@\xcd\xcc\xcc\xcc\xcc|S@\x00\x00\x00\x00\x06\x00\x00\x00\x02\x01\x03\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00=\n\xd7\xa3p=\x0e@\x8f\xc2\xf5(\\\x8f"@\x85\xebQ\xb8\x1e]`\xc0R\xb8\x1e\x85\xebQ\xf8?\x8f\xc2\xf5(\\\x8fA@\xe5\xd0"\xdb\xf9\x0eR@=\n\xd7\xa3p=\x0e@\x8f\xc2\xf5(\\\x8f"@\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x04@7.\x14z\xe1G\xae\xc0A%\x1e\xb8Q\xeb\x85\xbf\xf4\xf5\xc2\x8f\\(\xf6\xc0\x12p\xa3\xd7\n=q@\x0bG\xae\x14z\xe1H@Sz=p\xa3\xd7\n@7.\x14z\xe1G\xae\xc0A%\x1e\xb8Q\xeb\x85'

# format : WKB in hexa
POINT_WKB_HEX_BIG_ENDIAN = POINT_WKB_BIG_ENDIAN.hex()
POINT_EMPTY_WKB_HEX_BIG_ENDIAN = POINT_EMPTY_WKB_BIG_ENDIAN.hex()
LINESTRING_WKB_HEX_BIG_ENDIAN = LINESTRING_WKB_BIG_ENDIAN.hex()
LINESTRING_EMPTY_WKB_HEX_BIG_ENDIAN = LINESTRING_EMPTY_WKB_BIG_ENDIAN.hex()
POLYGON_WKB_HEX_BIG_ENDIAN = POLYGON_WKB_BIG_ENDIAN.hex()
POLYGON_EMPTY_WKB_HEX_BIG_ENDIAN = POLYGON_EMPTY_WKB_BIG_ENDIAN.hex()
MULTIPOINT_WKB_HEX_BIG_ENDIAN = MULTIPOINT_WKB_BIG_ENDIAN.hex()
MULTIPOINT_EMPTY_WKB_HEX_BIG_ENDIAN = MULTIPOINT_EMPTY_WKB_BIG_ENDIAN.hex()
MULTILINESTRING_WKB_HEX_BIG_ENDIAN = MULTILINESTRING_WKB_BIG_ENDIAN.hex()
MULTILINESTRING_EMPTY_WKB_HEX_BIG_ENDIAN = MULTILINESTRING_EMPTY_WKB_BIG_ENDIAN.hex()
MULTIPOLYGON_WKB_HEX_BIG_ENDIAN = MULTIPOLYGON_WKB_BIG_ENDIAN.hex()
MULTIPOLYGON_EMPTY_WKB_HEX_BIG_ENDIAN = MULTIPOLYGON_EMPTY_WKB_BIG_ENDIAN.hex()
GEOMETRYCOLLECTION_WKB_HEX_BIG_ENDIAN = GEOMETRYCOLLECTION_WKB_BIG_ENDIAN.hex()
GEOMETRYCOLLECTION_EMPTY_WKB_HEX_BIG_ENDIAN = (
    GEOMETRYCOLLECTION_EMPTY_WKB_BIG_ENDIAN.hex()
)
GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_HEX_BIG_ENDIAN = (
    GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_BIG_ENDIAN.hex()
)

# format : WKT
POINT_WKT = "POINT (-115.81 37.24)"
POINT_EMPTY_WKT = "POINT EMPTY"
LINESTRING_WKT = "LINESTRING (8.919 44.4074,8.923 44.4075)"
LINESTRING_EMPTY_WKT = "LINESTRING EMPTY"
POLYGON_WKT = "POLYGON ((2.38 57.322,23.194 -20.28,-120.43 19.15,2.38 57.322),(-5.21 23.51,15.21 -10.81,-20.51 1.51,-5.21 23.51))"
POLYGON_EMPTY_WKT = "POLYGON EMPTY"
MULTIPOINT_WKT = "MULTIPOINT (-155.52 19.61,-156.22 20.74,-157.97 21.46)"
MULTIPOINT_2_WKT = "MULTIPOINT ((-155.52 19.61),(-156.22 20.74),(-157.97 21.46))"
MULTIPOINT_EMPTY_WKT = "MULTIPOINT EMPTY"
MULTILINESTRING_WKT = (
    "MULTILINESTRING ((3.75 9.25,-130.95 1.52),(23.15 -34.25,-1.35 -4.65,3.45 77.95))"
)
MULTILINESTRING_EMPTY_WKT = "MULTILINESTRING EMPTY"
MULTIPOLYGON_WKT = "MULTIPOLYGON (((3.78 9.28,-130.91 1.52,35.12 72.234,3.78 9.28)),((23.18 -34.29,-1.31 -4.61,3.41 77.91,23.18 -34.29)))"
MULTIPOLYGON_EMPTY_WKT = "MULTIPOLYGON EMPTY"
GEOMETRYCOLLECTION_WKT = "GEOMETRYCOLLECTION (POINT (-115.81 37.24),LINESTRING (8.919 44.4074,8.923 44.4075),POLYGON ((2.38 57.322,23.194 -20.28,-120.43 19.15,2.38 57.322),(-5.21 23.51,15.21 -10.81,-20.51 1.51,-5.21 23.51)),MULTIPOINT (-155.52 19.61,-156.22 20.74,-157.97 21.46),MULTILINESTRING ((3.75 9.25,-130.95 1.52),(23.15 -34.25,-1.35 -4.65,3.45 77.95)),MULTIPOLYGON (((3.78 9.28,-130.91 1.52,35.12 72.234,3.78 9.28)),((23.18 -34.29,-1.31 -4.61,3.41 77.91,23.18 -34.29))))"
GEOMETRYCOLLECTION_EMPTY_WKT = "GEOMETRYCOLLECTION EMPTY"
GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKT = "GEOMETRYCOLLECTION (POINT EMPTY,LINESTRING (8.919 44.4074,8.923 44.4075),POLYGON ((2.38 57.322,23.194 -20.28,-120.43 19.15,2.38 57.322),(-5.21 23.51,15.21 -10.81,-20.51 1.51,-5.21 23.51)),MULTIPOINT EMPTY,MULTILINESTRING ((3.75 9.25,-130.95 1.52),(23.15 -34.25,-1.35 -4.65,3.45 77.95)),MULTIPOLYGON EMPTY)"

# "true" geometries
POINT_paris = {"type": "Point", "coordinates": [2.348860390484333, 48.85332408262766]}
LINESTRING_loire = {
    "type": "LineString",
    "coordinates": [
        [4.2242431640625, 44.83639545410477],
        [3.9825439453125, 44.83249999349062],
        [3.8726806640625, 44.96479793033101],
        [3.9166259765625, 45.182036837015886],
        [4.273681640625, 45.471688258104614],
        [4.1802978515625, 45.77135470445038],
        [3.9880371093749996, 46.01603873833416],
        [4.010009765624999, 46.479482189368646],
        [3.482666015625, 46.837649560937464],
        [2.955322265625, 47.2270293988673],
        [2.867431640625, 47.54687159892238],
        [1.7907714843749998, 47.89424772020999],
        [1.3623046875, 47.5913464767971],
        [0.6921386718749999, 47.39834920035926],
        [0.098876953125, 47.19717795172789],
        [-0.318603515625, 47.3834738721015],
        [-0.9558105468749999, 47.3834738721015],
        [-1.571044921875, 47.204642388766935],
        [-2.021484375, 47.301584511330795],
        [-2.186279296875, 47.27922900257082],
    ],
}
POLYGON_france = {
    "type": "Polygon",
    "coordinates": [
        [
            [2.4609375, 51.12421275782688],
            [1.7138671875, 50.875311142200765],
            [1.7138671875, 50.12057809796008],
            [0.3955078125, 49.781264058178344],
            [0.0439453125, 49.52520834197442],
            [0.3515625, 49.35375571830993],
            [-1.0986328125, 49.23912083246698],
            [-1.2744140625, 49.66762782262194],
            [-1.8017578124999998, 49.66762782262194],
            [-1.58203125, 49.23912083246698],
            [-1.3623046875, 48.60385760823255],
            [-2.5927734375, 48.45835188280866],
            [-3.0322265625, 48.777912755501845],
            [-4.6142578125, 48.66194284607006],
            [-4.74609375, 48.3416461723746],
            [-4.39453125, 48.37084770238366],
            [-4.21875, 48.16608541901253],
            [-4.6142578125, 48.07807894349862],
            [-4.350585937499999, 47.724544549099676],
            [-4.04296875, 47.989921667414194],
            [-2.8125, 47.69497434186282],
            [-2.021484375, 47.07012182383309],
            [-2.2412109375, 46.92025531537451],
            [-1.23046875, 46.28622391806706],
            [-1.0107421875, 45.767522962149876],
            [-0.6591796875, 45.120052841530544],
            [-1.142578125, 45.49094569262732],
            [-1.142578125, 44.37098696297173],
            [-1.7578125, 43.29320031385282],
            [0.5712890625, 42.65012181368022],
            [0.6591796875, 42.87596410238256],
            [1.8896484375, 42.45588764197166],
            [3.251953125, 42.35854391749705],
            [2.9443359375, 42.97250158602597],
            [4.1748046875, 43.51668853502906],
            [4.921875, 43.48481212891603],
            [5.9765625, 43.100982876188546],
            [6.459960937499999, 43.197167282501276],
            [7.55859375, 43.70759350405294],
            [7.6025390625, 44.08758502824516],
            [7.03125, 44.15068115978094],
            [6.723632812499999, 45.02695045318546],
            [6.9873046875, 45.61403741135093],
            [6.8994140625, 46.34692761055676],
            [6.15234375, 46.01222384063236],
            [6.1083984375, 46.49839225859763],
            [6.8115234375, 46.98025235521883],
            [7.55859375, 47.54687159892238],
            [7.646484374999999, 48.04870994288686],
            [8.2177734375, 48.980216985374994],
            [6.723632812499999, 49.095452162534826],
            [6.416015625, 49.468124067331644],
            [5.712890625, 49.410973199695846],
            [4.6142578125, 50.00773901463687],
            [2.900390625, 50.62507306341435],
            [2.4609375, 51.12421275782688],
        ]
    ],
}
MULTIPOINT_paris_tokyo = {
    "type": "MultiPoint",
    "coordinates": [[2.34886039048, 48.8533240826], [139.7530902922, 35.6853729713]],
}

MULTILINESTRING_loire_katsuragawa_river = {
    "type": "MultiLineString",
    "coordinates": [
        [
            [4.2242431640625, 44.83639545410477],
            [3.9825439453125, 44.83249999349062],
            [3.8726806640625, 44.96479793033101],
            [3.9166259765625, 45.182036837015886],
            [4.273681640625, 45.471688258104614],
            [4.1802978515625, 45.77135470445038],
            [3.9880371093749996, 46.01603873833416],
            [4.010009765624999, 46.479482189368646],
            [3.482666015625, 46.837649560937464],
            [2.955322265625, 47.2270293988673],
            [2.867431640625, 47.54687159892238],
            [1.7907714843749998, 47.89424772020999],
            [1.3623046875, 47.5913464767971],
            [0.6921386718749999, 47.39834920035926],
            [0.098876953125, 47.19717795172789],
            [-0.318603515625, 47.3834738721015],
            [-0.9558105468749999, 47.3834738721015],
            [-1.571044921875, 47.204642388766935],
            [-2.021484375, 47.301584511330795],
            [-2.186279296875, 47.27922900257082],
        ],
        [
            [135.4222869873047, 34.68291096793206],
            [135.50262451171875, 34.722426197808446],
            [135.61248779296875, 34.78899484825181],
            [135.68389892578125, 34.88705743313571],
            [135.73471069335938, 34.92422301690581],
            [135.73780059814453, 34.941392337729816],
            [135.70758819580078, 34.998222460984685],
            [135.69110870361328, 34.998222460984685],
            [135.6540298461914, 35.02999636902566],
            [135.57952880859375, 35.02212433874883],
            [135.54905891418457, 35.05262423302113],
            [135.51189422607422, 35.09266439952991],
            [135.51695823669434, 35.11653865167172],
            [135.49266815185547, 35.12917513034949],
            [135.5076026916504, 35.15121407216851],
            [135.51644325256348, 35.15345974393076],
            [135.51738739013672, 35.14665236059329],
            [135.53704261779782, 35.14430122477116],
            [135.54309368133545, 35.13215845728398],
            [135.56824207305908, 35.12829766045064],
            [135.57761907577515, 35.1388617696448],
            [135.5717396736145, 35.145582075842604],
            [135.58399200439453, 35.14419594844418],
            [135.60270309448242, 35.13844063537838],
            [135.60956954956055, 35.13212335995541],
            [135.6378936767578, 35.13984440779405],
            [135.63274383544922, 35.1540913279465],
            [135.64982414245605, 35.1707914371233],
            [135.6748867034912, 35.18664634969633],
            [135.68166732788086, 35.19667684282583],
            [135.70218086242676, 35.19836016087243],
            [135.70956230163574, 35.193029534057615],
            [135.7118797302246, 35.20256830337077],
            [135.71685791015625, 35.2116150714062],
            [135.72526931762695, 35.20130588351442],
            [135.736083984375, 35.21035279218927],
            [135.7476282119751, 35.20383070360394],
            [135.75419425964355, 35.20873985129727],
            [135.75912952423096, 35.201831894172635],
            [135.76183319091797, 35.20453202858757],
            [135.77406406402588, 35.20558400470673],
            [135.7796859741211, 35.221993067538584],
            [135.77805519104004, 35.23573485795656],
        ],
    ],
}


MULTIPOLYGON_france_japan = {
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [2.4609375, 51.12421275782688],
                [1.7138671875, 50.875311142200765],
                [1.7138671875, 50.12057809796008],
                [0.3955078125, 49.781264058178344],
                [0.0439453125, 49.52520834197442],
                [0.3515625, 49.35375571830993],
                [-1.0986328125, 49.23912083246698],
                [-1.2744140625, 49.66762782262194],
                [-1.8017578124999998, 49.66762782262194],
                [-1.58203125, 49.23912083246698],
                [-1.3623046875, 48.60385760823255],
                [-2.5927734375, 48.45835188280866],
                [-3.0322265625, 48.777912755501845],
                [-4.6142578125, 48.66194284607006],
                [-4.74609375, 48.3416461723746],
                [-4.39453125, 48.37084770238366],
                [-4.21875, 48.16608541901253],
                [-4.6142578125, 48.07807894349862],
                [-4.350585937499999, 47.724544549099676],
                [-4.04296875, 47.989921667414194],
                [-2.8125, 47.69497434186282],
                [-2.021484375, 47.07012182383309],
                [-2.2412109375, 46.92025531537451],
                [-1.23046875, 46.28622391806706],
                [-1.0107421875, 45.767522962149876],
                [-0.6591796875, 45.120052841530544],
                [-1.142578125, 45.49094569262732],
                [-1.142578125, 44.37098696297173],
                [-1.7578125, 43.29320031385282],
                [0.5712890625, 42.65012181368022],
                [0.6591796875, 42.87596410238256],
                [1.8896484375, 42.45588764197166],
                [3.251953125, 42.35854391749705],
                [2.9443359375, 42.97250158602597],
                [4.1748046875, 43.51668853502906],
                [4.921875, 43.48481212891603],
                [5.9765625, 43.100982876188546],
                [6.459960937499999, 43.197167282501276],
                [7.55859375, 43.70759350405294],
                [7.6025390625, 44.08758502824516],
                [7.03125, 44.15068115978094],
                [6.723632812499999, 45.02695045318546],
                [6.9873046875, 45.61403741135093],
                [6.8994140625, 46.34692761055676],
                [6.15234375, 46.01222384063236],
                [6.1083984375, 46.49839225859763],
                [6.8115234375, 46.98025235521883],
                [7.55859375, 47.54687159892238],
                [7.646484374999999, 48.04870994288686],
                [8.2177734375, 48.980216985374994],
                [6.723632812499999, 49.095452162534826],
                [6.416015625, 49.468124067331644],
                [5.712890625, 49.410973199695846],
                [4.6142578125, 50.00773901463687],
                [2.900390625, 50.62507306341435],
                [2.4609375, 51.12421275782688],
            ]
        ],
        [
            [
                [140.888671875, 41.52502957323801],
                [139.910888671875, 40.65563874006118],
                [140.042724609375, 39.45316112807394],
                [139.658203125, 38.58252615935333],
                [138.80126953125, 37.80544394934271],
                [137.26318359375, 36.73888412439431],
                [136.91162109374997, 37.055177106660814],
                [137.39501953124997, 37.47485808497102],
                [136.669921875, 37.38761749978395],
                [136.77978515625, 36.77409249464195],
                [135.90087890625, 35.97800618085566],
                [136.03271484375, 35.639441068973944],
                [135.46142578124997, 35.460669951495305],
                [135.2197265625, 35.8356283888737],
                [133.4619140625, 35.47856499535729],
                [133.1982421875, 35.585851593232356],
                [132.626953125, 35.47856499535729],
                [132.71484375, 35.22767235493586],
                [131.396484375, 34.43409789359469],
                [130.869140625, 34.34343606848294],
                [131.02294921875, 33.96158628979907],
                [131.7041015625, 34.05265942137599],
                [132.34130859375, 33.815666308702774],
                [132.34130859375, 34.415973384481866],
                [132.71484375, 34.288991865037524],
                [133.3740234375, 34.43409789359469],
                [133.857421875, 34.361576287484176],
                [134.47265625, 34.75966612466248],
                [135, 34.66935854524543],
                [135.3955078125, 34.75966612466248],
                [135.24169921875, 34.34343606848294],
                [135.63720703125, 33.44977658311846],
                [136.38427734375, 34.17999758688084],
                [136.86767578125, 34.470335121217474],
                [136.69189453125, 35.137879119634185],
                [137.48291015625, 34.66935854524543],
                [138.14208984375, 34.687427949314845],
                [138.88916015625, 35.22767235493586],
                [138.71337890625, 34.65128519895413],
                [139.19677734375, 34.994003757575776],
                [139.482421875, 35.35321610123823],
                [139.89990234375, 35.69299463209881],
                [140.18554687499997, 35.567980458012094],
                [139.8779296875, 35.209721645221386],
                [139.85595703125, 34.939985151560435],
                [140.44921875, 35.22767235493586],
                [140.537109375, 35.65729624809628],
                [140.8447265625, 35.746512259918504],
                [140.44921875, 36.20882309283712],
                [140.80078125, 36.94989178681327],
                [140.9326171875, 38.09998264736481],
                [141.17431640625, 38.47939467327645],
                [141.591796875, 38.35888785866677],
                [141.591796875, 38.95940879245423],
                [142.03125, 39.58875727696545],
                [141.7236328125, 40.463666324587685],
                [141.43798828125, 40.697299008636755],
                [141.4599609375, 41.45919537950706],
                [141.21826171875, 41.29431726315258],
                [140.888671875, 41.52502957323801],
            ]
        ],
        [
            [
                [141.8994140625, 45.460130637921004],
                [141.4599609375, 43.54854811091286],
                [140.712890625, 43.54854811091286],
                [140.5810546875, 42.97250158602597],
                [139.921875, 42.32606244456202],
                [140.0537109375, 41.21172151054787],
                [141.064453125, 41.73852846935917],
                [140.44921875, 42.32606244456202],
                [140.66894531249997, 42.61779143282346],
                [141.767578125, 42.65012181368022],
                [143.525390625, 41.934976500546604],
                [145.4150390625, 43.26120612479979],
                [145.283203125, 44.402391829093915],
                [143.3935546875, 44.24519901522129],
                [141.8994140625, 45.460130637921004],
            ]
        ],
        [
            [
                [134.1265869140625, 34.34343606848294],
                [133.8629150390625, 34.35704160076073],
                [133.670654296875, 34.20271636159618],
                [133.5552978515625, 33.99347299511967],
                [133.0938720703125, 33.89321737944089],
                [132.95104980468747, 34.11180455556899],
                [132.791748046875, 33.99347299511967],
                [132.681884765625, 33.77458136371689],
                [132.0391845703125, 33.367237465838315],
                [132.38525390625, 33.463525475613785],
                [132.36328125, 33.31216783738619],
                [132.5335693359375, 33.27543541298162],
                [132.5225830078125, 33.16054697509142],
                [132.5665283203125, 32.92109653816924],
                [132.6983642578125, 32.94875863715422],
                [132.6324462890625, 32.76880048488168],
                [132.8466796875, 32.778037985363675],
                [133.00048828125, 32.7503226078097],
                [133.011474609375, 33.04090311724091],
                [133.2806396484375, 33.243281858479484],
                [133.253173828125, 33.4039312002347],
                [133.7091064453125, 33.53681606773302],
                [134.000244140625, 33.445193134508465],
                [134.18701171875, 33.23409295522519],
                [134.36279296875, 33.62376800118811],
                [134.769287109375, 33.83848275599514],
                [134.5770263671875, 34.093610452768715],
                [134.615478515625, 34.21180215769026],
                [134.1265869140625, 34.34343606848294],
            ]
        ],
        [
            [
                [131.0009765625, 33.96500329452545],
                [130.8966064453125, 33.890367484132945],
                [130.5010986328125, 33.87497640410958],
                [130.308837890625, 33.57343808567733],
                [129.96826171875, 33.454359789517014],
                [129.8858642578125, 33.568861182555565],
                [129.84741210937497, 33.30757713015298],
                [129.4573974609375, 33.35347332342168],
                [129.3310546875, 33.137551192346145],
                [129.56726074218747, 33.23868752757414],
                [129.6551513671875, 33.054716488042736],
                [129.83642578125, 32.704111144407406],
                [129.7869873046875, 32.55607364492026],
                [130.1385498046875, 32.791892438123696],
                [130.155029296875, 32.69486597787505],
                [130.2703857421875, 32.60698915452777],
                [130.3253173828125, 32.92109653816924],
                [130.220947265625, 33.18813395605041],
                [130.6494140625, 32.7872745269555],
                [130.3692626953125, 32.523657815699146],
                [130.0286865234375, 32.46806060917602],
                [129.9957275390625, 32.189559980413584],
                [130.220947265625, 32.35212281198644],
                [130.62744140624997, 32.61161640317033],
                [130.341796875, 32.143059999988445],
                [130.1715087890625, 32.189559980413584],
                [130.1220703125, 32.10584293285769],
                [130.4296875, 31.541089879585808],
                [130.25390625, 31.39115752282472],
                [130.67138671875, 31.16580958786196],
                [130.693359375, 31.55981453201843],
                [130.869140625, 31.147006308556566],
                [131.0888671875, 31.44741029142872],
                [131.3525390625, 31.42866311735861],
                [131.7041015625, 32.43561304116276],
                [131.923828125, 32.97180377635759],
                [131.46240234375, 33.37641235124676],
                [131.81396484375, 33.50475906922609],
                [131.63818359375, 33.65120829920497],
                [131.1767578125, 33.52307880890422],
                [131.0009765625, 33.96500329452545],
            ]
        ],
    ],
}


GEOMETRYCOLLECTION_paris_tokyo_loire_katsuragawa_river_france_japan = {
    "type": "GeometryCollection",
    "geometries": [
        {
            "type": "MultiPoint",
            "coordinates": [
                [2.348860390484333, 48.85332408262766],
                [139.75309029221532, 35.68537297134676],
            ],
            "bbox": (
                2.348860390484333,
                35.68537297134676,
                139.75309029221532,
                48.85332408262766,
            ),
        },
        {
            "type": "MultiLineString",
            "coordinates": [
                [
                    [4.2242431640625, 44.83639545410477],
                    [3.9825439453125, 44.83249999349062],
                    [3.8726806640625, 44.96479793033101],
                    [3.9166259765625, 45.182036837015886],
                    [4.273681640625, 45.471688258104614],
                    [4.1802978515625, 45.77135470445038],
                    [3.9880371093749996, 46.01603873833416],
                    [4.010009765624999, 46.479482189368646],
                    [3.482666015625, 46.837649560937464],
                    [2.955322265625, 47.2270293988673],
                    [2.867431640625, 47.54687159892238],
                    [1.7907714843749998, 47.89424772020999],
                    [1.3623046875, 47.5913464767971],
                    [0.6921386718749999, 47.39834920035926],
                    [0.098876953125, 47.19717795172789],
                    [-0.318603515625, 47.3834738721015],
                    [-0.9558105468749999, 47.3834738721015],
                    [-1.571044921875, 47.204642388766935],
                    [-2.021484375, 47.301584511330795],
                    [-2.186279296875, 47.27922900257082],
                ],
                [
                    [135.4222869873047, 34.68291096793206],
                    [135.50262451171875, 34.722426197808446],
                    [135.61248779296875, 34.78899484825181],
                    [135.68389892578125, 34.88705743313571],
                    [135.73471069335938, 34.92422301690581],
                    [135.73780059814453, 34.941392337729816],
                    [135.70758819580078, 34.998222460984685],
                    [135.69110870361328, 34.998222460984685],
                    [135.6540298461914, 35.02999636902566],
                    [135.57952880859375, 35.02212433874883],
                    [135.54905891418457, 35.05262423302113],
                    [135.51189422607422, 35.09266439952991],
                    [135.51695823669434, 35.11653865167172],
                    [135.49266815185547, 35.12917513034949],
                    [135.5076026916504, 35.15121407216851],
                    [135.51644325256348, 35.15345974393076],
                    [135.51738739013672, 35.14665236059329],
                    [135.53704261779782, 35.14430122477116],
                    [135.54309368133545, 35.13215845728398],
                    [135.56824207305908, 35.12829766045064],
                    [135.57761907577515, 35.1388617696448],
                    [135.5717396736145, 35.145582075842604],
                    [135.58399200439453, 35.14419594844418],
                    [135.60270309448242, 35.13844063537838],
                    [135.60956954956055, 35.13212335995541],
                    [135.6378936767578, 35.13984440779405],
                    [135.63274383544922, 35.1540913279465],
                    [135.64982414245605, 35.1707914371233],
                    [135.6748867034912, 35.18664634969633],
                    [135.68166732788086, 35.19667684282583],
                    [135.70218086242676, 35.19836016087243],
                    [135.70956230163574, 35.193029534057615],
                    [135.7118797302246, 35.20256830337077],
                    [135.71685791015625, 35.2116150714062],
                    [135.72526931762695, 35.20130588351442],
                    [135.736083984375, 35.21035279218927],
                    [135.7476282119751, 35.20383070360394],
                    [135.75419425964355, 35.20873985129727],
                    [135.75912952423096, 35.201831894172635],
                    [135.76183319091797, 35.20453202858757],
                    [135.77406406402588, 35.20558400470673],
                    [135.7796859741211, 35.221993067538584],
                    [135.77805519104004, 35.23573485795656],
                ],
            ],
            "bbox": (
                -2.186279296875,
                34.68291096793206,
                135.7796859741211,
                47.89424772020999,
            ),
        },
        {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [2.4609375, 51.12421275782688],
                        [1.7138671875, 50.875311142200765],
                        [1.7138671875, 50.12057809796008],
                        [0.3955078125, 49.781264058178344],
                        [0.0439453125, 49.52520834197442],
                        [0.3515625, 49.35375571830993],
                        [-1.0986328125, 49.23912083246698],
                        [-1.2744140625, 49.66762782262194],
                        [-1.8017578124999998, 49.66762782262194],
                        [-1.58203125, 49.23912083246698],
                        [-1.3623046875, 48.60385760823255],
                        [-2.5927734375, 48.45835188280866],
                        [-3.0322265625, 48.777912755501845],
                        [-4.6142578125, 48.66194284607006],
                        [-4.74609375, 48.3416461723746],
                        [-4.39453125, 48.37084770238366],
                        [-4.21875, 48.16608541901253],
                        [-4.6142578125, 48.07807894349862],
                        [-4.350585937499999, 47.724544549099676],
                        [-4.04296875, 47.989921667414194],
                        [-2.8125, 47.69497434186282],
                        [-2.021484375, 47.07012182383309],
                        [-2.2412109375, 46.92025531537451],
                        [-1.23046875, 46.28622391806706],
                        [-1.0107421875, 45.767522962149876],
                        [-0.6591796875, 45.120052841530544],
                        [-1.142578125, 45.49094569262732],
                        [-1.142578125, 44.37098696297173],
                        [-1.7578125, 43.29320031385282],
                        [0.5712890625, 42.65012181368022],
                        [0.6591796875, 42.87596410238256],
                        [1.8896484375, 42.45588764197166],
                        [3.251953125, 42.35854391749705],
                        [2.9443359375, 42.97250158602597],
                        [4.1748046875, 43.51668853502906],
                        [4.921875, 43.48481212891603],
                        [5.9765625, 43.100982876188546],
                        [6.459960937499999, 43.197167282501276],
                        [7.55859375, 43.70759350405294],
                        [7.6025390625, 44.08758502824516],
                        [7.03125, 44.15068115978094],
                        [6.723632812499999, 45.02695045318546],
                        [6.9873046875, 45.61403741135093],
                        [6.8994140625, 46.34692761055676],
                        [6.15234375, 46.01222384063236],
                        [6.1083984375, 46.49839225859763],
                        [6.8115234375, 46.98025235521883],
                        [7.55859375, 47.54687159892238],
                        [7.646484374999999, 48.04870994288686],
                        [8.2177734375, 48.980216985374994],
                        [6.723632812499999, 49.095452162534826],
                        [6.416015625, 49.468124067331644],
                        [5.712890625, 49.410973199695846],
                        [4.6142578125, 50.00773901463687],
                        [2.900390625, 50.62507306341435],
                        [2.4609375, 51.12421275782688],
                    ]
                ],
                [
                    [
                        [140.888671875, 41.52502957323801],
                        [139.910888671875, 40.65563874006118],
                        [140.042724609375, 39.45316112807394],
                        [139.658203125, 38.58252615935333],
                        [138.80126953125, 37.80544394934271],
                        [137.26318359375, 36.73888412439431],
                        [136.91162109374997, 37.055177106660814],
                        [137.39501953124997, 37.47485808497102],
                        [136.669921875, 37.38761749978395],
                        [136.77978515625, 36.77409249464195],
                        [135.90087890625, 35.97800618085566],
                        [136.03271484375, 35.639441068973944],
                        [135.46142578124997, 35.460669951495305],
                        [135.2197265625, 35.8356283888737],
                        [133.4619140625, 35.47856499535729],
                        [133.1982421875, 35.585851593232356],
                        [132.626953125, 35.47856499535729],
                        [132.71484375, 35.22767235493586],
                        [131.396484375, 34.43409789359469],
                        [130.869140625, 34.34343606848294],
                        [131.02294921875, 33.96158628979907],
                        [131.7041015625, 34.05265942137599],
                        [132.34130859375, 33.815666308702774],
                        [132.34130859375, 34.415973384481866],
                        [132.71484375, 34.288991865037524],
                        [133.3740234375, 34.43409789359469],
                        [133.857421875, 34.361576287484176],
                        [134.47265625, 34.75966612466248],
                        [135, 34.66935854524543],
                        [135.3955078125, 34.75966612466248],
                        [135.24169921875, 34.34343606848294],
                        [135.63720703125, 33.44977658311846],
                        [136.38427734375, 34.17999758688084],
                        [136.86767578125, 34.470335121217474],
                        [136.69189453125, 35.137879119634185],
                        [137.48291015625, 34.66935854524543],
                        [138.14208984375, 34.687427949314845],
                        [138.88916015625, 35.22767235493586],
                        [138.71337890625, 34.65128519895413],
                        [139.19677734375, 34.994003757575776],
                        [139.482421875, 35.35321610123823],
                        [139.89990234375, 35.69299463209881],
                        [140.18554687499997, 35.567980458012094],
                        [139.8779296875, 35.209721645221386],
                        [139.85595703125, 34.939985151560435],
                        [140.44921875, 35.22767235493586],
                        [140.537109375, 35.65729624809628],
                        [140.8447265625, 35.746512259918504],
                        [140.44921875, 36.20882309283712],
                        [140.80078125, 36.94989178681327],
                        [140.9326171875, 38.09998264736481],
                        [141.17431640625, 38.47939467327645],
                        [141.591796875, 38.35888785866677],
                        [141.591796875, 38.95940879245423],
                        [142.03125, 39.58875727696545],
                        [141.7236328125, 40.463666324587685],
                        [141.43798828125, 40.697299008636755],
                        [141.4599609375, 41.45919537950706],
                        [141.21826171875, 41.29431726315258],
                        [140.888671875, 41.52502957323801],
                    ]
                ],
                [
                    [
                        [141.8994140625, 45.460130637921004],
                        [141.4599609375, 43.54854811091286],
                        [140.712890625, 43.54854811091286],
                        [140.5810546875, 42.97250158602597],
                        [139.921875, 42.32606244456202],
                        [140.0537109375, 41.21172151054787],
                        [141.064453125, 41.73852846935917],
                        [140.44921875, 42.32606244456202],
                        [140.66894531249997, 42.61779143282346],
                        [141.767578125, 42.65012181368022],
                        [143.525390625, 41.934976500546604],
                        [145.4150390625, 43.26120612479979],
                        [145.283203125, 44.402391829093915],
                        [143.3935546875, 44.24519901522129],
                        [141.8994140625, 45.460130637921004],
                    ]
                ],
                [
                    [
                        [134.1265869140625, 34.34343606848294],
                        [133.8629150390625, 34.35704160076073],
                        [133.670654296875, 34.20271636159618],
                        [133.5552978515625, 33.99347299511967],
                        [133.0938720703125, 33.89321737944089],
                        [132.95104980468747, 34.11180455556899],
                        [132.791748046875, 33.99347299511967],
                        [132.681884765625, 33.77458136371689],
                        [132.0391845703125, 33.367237465838315],
                        [132.38525390625, 33.463525475613785],
                        [132.36328125, 33.31216783738619],
                        [132.5335693359375, 33.27543541298162],
                        [132.5225830078125, 33.16054697509142],
                        [132.5665283203125, 32.92109653816924],
                        [132.6983642578125, 32.94875863715422],
                        [132.6324462890625, 32.76880048488168],
                        [132.8466796875, 32.778037985363675],
                        [133.00048828125, 32.7503226078097],
                        [133.011474609375, 33.04090311724091],
                        [133.2806396484375, 33.243281858479484],
                        [133.253173828125, 33.4039312002347],
                        [133.7091064453125, 33.53681606773302],
                        [134.000244140625, 33.445193134508465],
                        [134.18701171875, 33.23409295522519],
                        [134.36279296875, 33.62376800118811],
                        [134.769287109375, 33.83848275599514],
                        [134.5770263671875, 34.093610452768715],
                        [134.615478515625, 34.21180215769026],
                        [134.1265869140625, 34.34343606848294],
                    ]
                ],
                [
                    [
                        [131.0009765625, 33.96500329452545],
                        [130.8966064453125, 33.890367484132945],
                        [130.5010986328125, 33.87497640410958],
                        [130.308837890625, 33.57343808567733],
                        [129.96826171875, 33.454359789517014],
                        [129.8858642578125, 33.568861182555565],
                        [129.84741210937497, 33.30757713015298],
                        [129.4573974609375, 33.35347332342168],
                        [129.3310546875, 33.137551192346145],
                        [129.56726074218747, 33.23868752757414],
                        [129.6551513671875, 33.054716488042736],
                        [129.83642578125, 32.704111144407406],
                        [129.7869873046875, 32.55607364492026],
                        [130.1385498046875, 32.791892438123696],
                        [130.155029296875, 32.69486597787505],
                        [130.2703857421875, 32.60698915452777],
                        [130.3253173828125, 32.92109653816924],
                        [130.220947265625, 33.18813395605041],
                        [130.6494140625, 32.7872745269555],
                        [130.3692626953125, 32.523657815699146],
                        [130.0286865234375, 32.46806060917602],
                        [129.9957275390625, 32.189559980413584],
                        [130.220947265625, 32.35212281198644],
                        [130.62744140624997, 32.61161640317033],
                        [130.341796875, 32.143059999988445],
                        [130.1715087890625, 32.189559980413584],
                        [130.1220703125, 32.10584293285769],
                        [130.4296875, 31.541089879585808],
                        [130.25390625, 31.39115752282472],
                        [130.67138671875, 31.16580958786196],
                        [130.693359375, 31.55981453201843],
                        [130.869140625, 31.147006308556566],
                        [131.0888671875, 31.44741029142872],
                        [131.3525390625, 31.42866311735861],
                        [131.7041015625, 32.43561304116276],
                        [131.923828125, 32.97180377635759],
                        [131.46240234375, 33.37641235124676],
                        [131.81396484375, 33.50475906922609],
                        [131.63818359375, 33.65120829920497],
                        [131.1767578125, 33.52307880890422],
                        [131.0009765625, 33.96500329452545],
                    ]
                ],
            ],
            "bbox": (
                -4.74609375,
                31.147006308556566,
                145.4150390625,
                51.12421275782688,
            ),
        },
    ],
    "bbox": (-4.74609375, 31.147006308556566, 145.4150390625, 51.12421275782688),
}


# testing geometry

test_polygon_a = {
    "type": "Polygon",
    "coordinates": [[[-2, -2], [-2, 2], [2, 2], [2, -2], [-2, -2]]],
}
test_polygon_b = {
    "type": "Polygon",
    "coordinates": [[[-1, -3], [-1, 1], [3, 1], [3, -3], [-1, -3]]],
}
test_polygon_c = {
    "type": "Polygon",
    "coordinates": [[[2, 2], [2, 4], [4, 4], [4, 2], [2, 2]]],
}

