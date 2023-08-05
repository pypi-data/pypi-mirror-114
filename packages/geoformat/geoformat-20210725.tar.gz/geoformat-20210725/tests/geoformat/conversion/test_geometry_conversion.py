from geoformat.conversion.geometry_conversion import (
    geometry_type_to_2d_geometry_type,
    geometry_to_2d_geometry,
    geometry_to_geometry_collection,
    single_geometry_to_multi_geometry,
    multi_geometry_to_single_geometry,
    geometry_to_multi_geometry,
    wkb_to_geometry,
    geometry_to_wkb,
    wkt_to_geometry,
    geometry_to_wkt,
    force_rhr,
    geometry_to_bbox,
    reproject_geometry,
    geometry_to_ogr_geometry,
    ogr_geometry_to_geometry
)

from tests.data.geometries import (
    POINT,
    POINT_EMPTY,
    MULTIPOINT,
    MULTIPOINT_EMPTY,
    LINESTRING,
    LINESTRING_EMPTY,
    MULTILINESTRING,
    MULTILINESTRING_EMPTY,
    POLYGON,
    POLYGON_EMPTY,
    MULTIPOLYGON,
    MULTIPOLYGON_EMPTY,
    GEOMETRYCOLLECTION,
    GEOMETRYCOLLECTION_EMPTY,
    GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
    POINT_WITH_BBOX,
    MULTIPOINT_WITH_BBOX,
    LINESTRING_WITH_BBOX,
    MULTILINESTRING_WITH_BBOX,
    POLYGON_WITH_BBOX,
    MULTIPOLYGON_WITH_BBOX,
    GEOMETRYCOLLECTION_WITH_BBOX,
    GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WITH_BBOX,
    POINT_WKB_BIG_ENDIAN,
    LINESTRING_WKB_BIG_ENDIAN,
    POLYGON_WKB_BIG_ENDIAN,
    MULTIPOINT_WKB_BIG_ENDIAN,
    MULTILINESTRING_WKB_BIG_ENDIAN,
    MULTIPOLYGON_WKB_BIG_ENDIAN,
    GEOMETRYCOLLECTION_WKB_BIG_ENDIAN,
    POINT_WKB_LITTLE_ENDIAN,
    LINESTRING_WKB_LITTLE_ENDIAN,
    POLYGON_WKB_LITTLE_ENDIAN,
    MULTIPOINT_WKB_LITTLE_ENDIAN,
    MULTILINESTRING_WKB_LITTLE_ENDIAN,
    MULTIPOLYGON_WKB_LITTLE_ENDIAN,
    GEOMETRYCOLLECTION_WKB_LITTLE_ENDIAN,
    MULTIPOINT_WKB_VARYING_ENDIAN,
    MULTILINESTRING_WKB_VARYING_ENDIAN,
    MULTIPOLYGON_WKB_VARYING_ENDIAN,
    GEOMETRYCOLLECTION_WKB_VARYING_ENDIAN,
    POINT_EMPTY_WKB_BIG_ENDIAN,
    POINT_EMPTY_WKB_LITTLE_ENDIAN,
    LINESTRING_EMPTY_WKB_BIG_ENDIAN,
    LINESTRING_EMPTY_WKB_LITTLE_ENDIAN,
    POLYGON_EMPTY_WKB_BIG_ENDIAN,
    POLYGON_EMPTY_WKB_LITTLE_ENDIAN,
    MULTIPOINT_EMPTY_WKB_BIG_ENDIAN,
    MULTIPOINT_EMPTY_WKB_LITTLE_ENDIAN,
    MULTILINESTRING_EMPTY_WKB_BIG_ENDIAN,
    MULTILINESTRING_EMPTY_WKB_LITTLE_ENDIAN,
    MULTIPOLYGON_EMPTY_WKB_BIG_ENDIAN,
    MULTIPOLYGON_EMPTY_WKB_LITTLE_ENDIAN,
    GEOMETRYCOLLECTION_EMPTY_WKB_BIG_ENDIAN,
    GEOMETRYCOLLECTION_EMPTY_WKB_LITTLE_ENDIAN,
    GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_BIG_ENDIAN,
    GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_LITTLE_ENDIAN,
    POINT_WKT,
    POINT_EMPTY_WKT,
    LINESTRING_WKT,
    LINESTRING_EMPTY_WKT,
    POLYGON_WKT,
    POLYGON_EMPTY_WKT,
    MULTIPOINT_WKT,
    MULTIPOINT_EMPTY_WKT,
    MULTILINESTRING_WKT,
    MULTILINESTRING_EMPTY_WKT,
    MULTIPOLYGON_WKT,
    MULTIPOLYGON_EMPTY_WKT,
    GEOMETRYCOLLECTION_WKT,
    GEOMETRYCOLLECTION_EMPTY_WKT,
    GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKT,
    POINT_3D,
    LINESTRING_3D,
    POLYGON_3D,
    MULTIPOINT_3D,
    MULTILINESTRING_3D,
    MULTIPOLYGON_3D,
    GEOMETRYCOLLECTION_3D,
    POINT_paris,
    LINESTRING_loire,
    POLYGON_france,
    MULTIPOINT_paris_tokyo,
    MULTILINESTRING_loire_katsuragawa_river,
    MULTIPOLYGON_france_japan,
    GEOMETRYCOLLECTION_paris_tokyo_loire_katsuragawa_river_france_japan
)

from test_all import (
    test_function,
    test_dependencies
)

try:
    from osgeo import ogr
except ImportError:
    pass


geometry_type_to_2d_geometry_type_parameters = {
    0: {
        "geometry_type": "POINT",
        "return_value": "Point"
    },
    1: {
        "geometry_type": "Linestring",
        "return_value": "LineString"
    },
    2: {
        "geometry_type": "Polygon",
        "return_value": "Polygon"
    },
    3: {
        "geometry_type": "multipoint",
        "return_value": "MultiPoint"
    },
    4: {
        "geometry_type": "MultiLInestring",
        "return_value": "MultiLineString"
    },
    5: {
        "geometry_type": "MultiPolygon",
        "return_value": "MultiPolygon"
    },
    6: {
        "geometry_type": "MultiPolygon",
        "return_value": "MultiPolygon"
    },
    7: {
        "geometry_type": "GEOMETRYCOLLECTION",
        "return_value": "GeometryCollection"
    },
    8: {
        "geometry_type": "Point25D",
        "return_value": "Point"
    },
    9: {
        "geometry_type": "LineString25D",
        "return_value": "LineString"
    },
    10: {
        "geometry_type": "Polygon25D",
        "return_value": "Polygon"
    },
    11: {
        "geometry_type": "MultiPoint25D",
        "return_value": "MultiPoint"
    },
    12: {
        "geometry_type": "MultiLineString25D",
        "return_value": "MultiLineString"
    },
    13: {
        "geometry_type": "MultiPolygon25D",
        "return_value": "MultiPolygon"
    },
}

geometry_to_2d_geometry_parameters = {
    0: {
        "geometry": POINT_3D,
        "bbox": False,
        "return_value": POINT
    },
    1: {
        "geometry": LINESTRING_3D,
        "bbox": False,
        "return_value": LINESTRING
    },
    2: {
        "geometry": POLYGON_3D,
        "bbox": False,
        "return_value": POLYGON
    },
    3: {
        "geometry": MULTIPOINT_3D,
        "bbox": False,
        "return_value": MULTIPOINT
    },
    4: {
        "geometry": MULTILINESTRING_3D,
        "bbox": False,
        "return_value": MULTILINESTRING
    },
    5: {
        "geometry": MULTIPOLYGON_3D,
        "bbox": False,
        "return_value": MULTIPOLYGON
    },
    6: {
        "geometry": GEOMETRYCOLLECTION_3D,
        "bbox": False,
        "return_value": GEOMETRYCOLLECTION
    }
}

geometry_to_geometry_collection_parameters = {
    0: {
        "geometry": POINT,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [POINT_WITH_BBOX], "bbox": POINT_WITH_BBOX['bbox']}
    },
    1: {
        "geometry": LINESTRING,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [LINESTRING_WITH_BBOX], "bbox": LINESTRING_WITH_BBOX['bbox']}
    },
    2: {
        "geometry": POLYGON,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [POLYGON_WITH_BBOX], "bbox": POLYGON_WITH_BBOX['bbox']}
    },
    3: {
        "geometry": MULTIPOINT,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [MULTIPOINT_WITH_BBOX], "bbox": MULTIPOINT_WITH_BBOX['bbox']}
    },
    4: {
        "geometry": MULTILINESTRING,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [MULTILINESTRING_WITH_BBOX], "bbox": MULTILINESTRING_WITH_BBOX['bbox']}
    },
    5: {
        "geometry": MULTIPOLYGON,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [MULTIPOLYGON_WITH_BBOX], "bbox": MULTIPOLYGON_WITH_BBOX['bbox']}
    },
    6: {
        "geometry": GEOMETRYCOLLECTION,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": GEOMETRYCOLLECTION_WITH_BBOX
    },
    7: {
        "geometry": POINT_EMPTY,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [POINT_EMPTY]}
    },
    8: {
        "geometry": LINESTRING_EMPTY,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [LINESTRING_EMPTY]}
    },
    9: {
        "geometry": POLYGON_EMPTY,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [POLYGON_EMPTY]}
    },
    10: {
        "geometry": MULTIPOINT_EMPTY,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [MULTIPOINT_EMPTY]}
    },
    11: {
        "geometry": MULTILINESTRING_EMPTY,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [MULTILINESTRING_EMPTY]}
    },
    12: {
        "geometry": MULTIPOLYGON_EMPTY,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {"type": "GeometryCollection", "geometries": [MULTIPOLYGON_EMPTY]}
    },
    13: {
        "geometry": GEOMETRYCOLLECTION_EMPTY,
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": GEOMETRYCOLLECTION_EMPTY
    },
    14: {
        "geometry": {'type': 'GeometryCollection', 'geometries': [{'type': 'Polygon', 'coordinates': []}]},
        "geometry_type_filter": None,
        "bbox": True,
        "return_value": {'type': 'GeometryCollection', 'geometries': [{'type': 'Polygon', 'coordinates': []}]}
    }
}

geometry_to_multi_geometry_parameters = {
    0: {"geometry": POINT,
        "bbox": False,
        "return_value": {'type': "MultiPoint", "coordinates": [POINT['coordinates']]}
    },
    1: {"geometry": LINESTRING,
        "bbox": False,
        "return_value": {"type": "MultiLineString", "coordinates": [LINESTRING['coordinates']]}
    },
    2: {"geometry": POLYGON,
        "bbox": False,
        "return_value":  {"type": "MultiPolygon", "coordinates": [POLYGON['coordinates']]}
    },
    3: {
        "geometry": MULTIPOINT,
        "bbox": False,
        "return_value": MULTIPOINT
    },
    4: {
        "geometry": MULTILINESTRING,
        "bbox": False,
        "return_value": MULTILINESTRING
    },
    5: {
        "geometry": MULTIPOLYGON,
        "bbox": False,
        "return_value": MULTIPOLYGON
    },
    6: {
        "geometry": GEOMETRYCOLLECTION,
        "bbox": False,
        "return_value": {"type": "GeometryCollection", "geometries": [
            {"type": "MultiPoint", "coordinates": [[-115.81, 37.24]]},
            {"type": "MultiLineString", "coordinates": [[[8.919, 44.4074], [8.923, 44.4075]]]},
            {"type": "MultiPolygon", "coordinates": [[[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]]]},
            {"type": "MultiPoint", "coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]]},
            {"type": "MultiLineString", "coordinates": [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]]},
            {"type": "MultiPolygon", "coordinates": [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]]}
        ]
        }
    },
    7: {"geometry": POINT,
        "bbox": True,
        "return_value": {'type': "MultiPoint", "coordinates": [POINT_WITH_BBOX['coordinates']], "bbox": POINT_WITH_BBOX["bbox"]}
        },
    8: {"geometry": LINESTRING,
        "bbox": True,
        "return_value": {"type": "MultiLineString", "coordinates": [LINESTRING_WITH_BBOX['coordinates']], "bbox": LINESTRING_WITH_BBOX["bbox"]}
        },
    9: {"geometry": POLYGON,
        "bbox": True,
        "return_value": {"type": "MultiPolygon", "coordinates": [POLYGON_WITH_BBOX['coordinates']], "bbox": POLYGON_WITH_BBOX["bbox"]}
        },
    10: {
        "geometry": MULTIPOINT,
        "bbox": True,
        "return_value": MULTIPOINT_WITH_BBOX
    },
    11: {
        "geometry": MULTILINESTRING,
        "bbox": True,
        "return_value": MULTILINESTRING_WITH_BBOX
    },
    12: {
        "geometry": MULTIPOLYGON,
        "bbox": True,
        "return_value": MULTIPOLYGON_WITH_BBOX
    },
    13: {
        "geometry": GEOMETRYCOLLECTION,
        "bbox": True,
        "return_value": {'type': 'GeometryCollection',
                         'geometries': [
                            {'type': 'MultiPoint', 'coordinates': [[-115.81, 37.24]], 'bbox': (-115.81, 37.24, -115.81, 37.24)},
                            {'type': 'MultiLineString', 'coordinates': [[[8.919, 44.4074], [8.923, 44.4075]]], 'bbox': (8.919, 44.4074, 8.923, 44.4075)},
                            {'type': 'MultiPolygon', 'coordinates': [[[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]]], 'bbox': (-120.43, -20.28, 23.194, 57.322)},
                            {'type': 'MultiPoint', 'coordinates': [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]], 'bbox': (-157.97, 19.61, -155.52, 21.46)},
                            {'type': 'MultiLineString', 'coordinates': [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]], 'bbox': (-130.95, -34.25, 23.15, 77.95)},
                            {'type': 'MultiPolygon', 'coordinates': [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]], 'bbox': (-130.91, -34.29, 35.12, 77.91)}
                        ],
                        'bbox': (-157.97, -34.29, 35.12, 77.95)}
    },
}

single_geometry_to_multi_geometry_parameters = {
    0: {
        "geometry": POINT,
        "bbox": False,
        "return_value": {"type": "MultiPoint", "coordinates": [POINT["coordinates"]]}
    },
    1: {
        "geometry": LINESTRING,
        "bbox": False,
        "return_value": {"type": "MultiLineString", "coordinates": [LINESTRING["coordinates"]]}
    },
    2: {
        "geometry": POLYGON,
        "bbox": False,
        "return_value": {"type": "MultiPolygon", "coordinates": [POLYGON["coordinates"]]}
    },
    3: {
        "geometry": GEOMETRYCOLLECTION,
        "bbox": False,
        "return_value": {"type": "GeometryCollection", "geometries": [{"type": "MultiPoint", "coordinates": [[-115.81, 37.24]]}, {"type": "MultiLineString", "coordinates": [[[8.919, 44.4074], [8.923, 44.4075]]]}, {"type": "MultiPolygon", "coordinates": [[[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]]]}, {"type": "MultiPoint", "coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]]}, {"type": "MultiLineString", "coordinates": [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]]}, {"type": "MultiPolygon", "coordinates": [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]]}]}
    },
    4: {
        "geometry": POINT,
        "bbox": True,
        "return_value": {"type": "MultiPoint", "coordinates": [POINT["coordinates"]], "bbox": POINT_WITH_BBOX['bbox']}
    },
    5: {
        "geometry": LINESTRING,
        "bbox": True,
        "return_value": {"type": "MultiLineString", "coordinates": [LINESTRING["coordinates"]], "bbox": LINESTRING_WITH_BBOX['bbox']}
    },
    6: {
        "geometry": POLYGON,
        "bbox": True,
        "return_value": {"type": "MultiPolygon", "coordinates": [POLYGON["coordinates"]], "bbox": POLYGON_WITH_BBOX['bbox']}
    },
    7: {
        "geometry": GEOMETRYCOLLECTION,
        "bbox": True,
        "return_value": {
            "type": "GeometryCollection",
            "geometries": [
                {
                    "type": "MultiPoint",
                    "coordinates": [[-115.81, 37.24]],
                    "bbox": GEOMETRYCOLLECTION_WITH_BBOX['geometries'][0]['bbox']
                },
                {
                    "type": "MultiLineString",
                    "coordinates": [[[8.919, 44.4074], [8.923, 44.4075]]],
                    "bbox": GEOMETRYCOLLECTION_WITH_BBOX['geometries'][1]['bbox']
                },
                {
                    "type": "MultiPolygon",
                    "coordinates": [[[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]]],
                    "bbox": GEOMETRYCOLLECTION_WITH_BBOX['geometries'][2]['bbox']
                },
                {
                    "type": "MultiPoint",
                    "coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]],
                    "bbox": GEOMETRYCOLLECTION_WITH_BBOX['geometries'][3]['bbox']
                },
                {
                    "type": "MultiLineString",
                    "coordinates": [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]],
                    "bbox": GEOMETRYCOLLECTION_WITH_BBOX['geometries'][4]['bbox']
                },
                {
                    "type": "MultiPolygon",
                    "coordinates": [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]],
                    "bbox": GEOMETRYCOLLECTION_WITH_BBOX['geometries'][5]['bbox']
                }
            ],
        "bbox": GEOMETRYCOLLECTION_WITH_BBOX['bbox']
        }
    },
}

multi_geometry_to_single_geometry_parameters = {
    0: {"geometry": POINT,
        "bbox": False,
        "return_value": (POINT,)},
    1: {"geometry": LINESTRING,
        "bbox": False,
        "return_value": (LINESTRING,)},
    2: {"geometry": POLYGON,
        "bbox": False,
        "return_value": (POLYGON,)},
    3: {
        "geometry": MULTIPOINT,
        "bbox": False,
        "return_value": (
            {"type": "Point", "coordinates": [-155.52, 19.61]},
            {"type": "Point", "coordinates": [-156.22, 20.74]},
            {"type": "Point", "coordinates": [-157.97, 21.46]},
        ),
    },
    4: {
        "geometry": MULTILINESTRING,
        "bbox": False,
        "return_value": (
            {"type": "LineString", "coordinates": [[3.75, 9.25], [-130.95, 1.52]]},
            {
                "type": "LineString",
                "coordinates": [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]],
            },
        ),
    },
    5: {
        "geometry": MULTIPOLYGON,
        "bbox": False,
        "return_value": (
            {
                "type": "Polygon",
                "coordinates": [
                    [[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]
                ],
            },
            {
                "type": "Polygon",
                "coordinates": [
                    [[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]
                ],
            },
        ),
    },
    6: {
        "geometry": GEOMETRYCOLLECTION,
        "bbox": False,
        "return_value": (
            {"type": "Point", "coordinates": [-115.81, 37.24]},
            {"type": "LineString", "coordinates": [[8.919, 44.4074], [8.923, 44.4075]]},
            {"type": "Polygon", "coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]]},
            {"type": "Point", "coordinates": [-155.52, 19.61]},
            {"type": "Point", "coordinates": [-156.22, 20.74]},
            {"type": "Point", "coordinates": [-157.97, 21.46]},
            {"type": "LineString", "coordinates": [[3.75, 9.25], [-130.95, 1.52]]},
            {"type": "LineString", "coordinates": [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]},
            {"type": "Polygon", "coordinates": [[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]]},
            {"type": "Polygon", "coordinates": [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]}
        )
    },
    7: {"geometry": POINT,
        "bbox": True,
        "return_value": (POINT_WITH_BBOX,)},
    8: {"geometry": LINESTRING,
        "bbox": True,
        "return_value": (LINESTRING_WITH_BBOX,)},
    9: {"geometry": POLYGON,
        "bbox": True,
        "return_value": (POLYGON_WITH_BBOX,)},
    10: {
        "geometry": MULTIPOINT,
        "bbox": True,
        "return_value": (
            {"type": "Point", "coordinates": [-155.52, 19.61], "bbox": (-155.52, 19.61, -155.52, 19.61)},
            {"type": "Point", "coordinates": [-156.22, 20.74], "bbox": (-156.22, 20.74, -156.22, 20.74)},
            {"type": "Point", "coordinates": [-157.97, 21.46], "bbox": (-157.97, 21.46, -157.97, 21.46)},
        ),
    },
    11: {
        "geometry": MULTILINESTRING,
        "bbox": True,
        "return_value": (
            {"type": "LineString", "coordinates": [[3.75, 9.25], [-130.95, 1.52]], "bbox": (-130.95, 1.52, 3.75, 9.25)},
            {"type": "LineString", "coordinates": [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]], "bbox": (-1.35, -34.25, 23.15, 77.95)},
        ),
    },
    12: {
        "geometry": MULTIPOLYGON,
        "bbox": True,
        "return_value": (
            {"type": "Polygon", "coordinates": [[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], "bbox": (-130.91, 1.52, 35.12, 72.234)},
            {"type": "Polygon", "coordinates": [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]], "bbox": (-1.31, -34.29, 23.18, 77.91)},
        ),
    },
    13: {
        "geometry": GEOMETRYCOLLECTION,
        "bbox": True,
        "return_value": (
            {"type": "Point", "coordinates": [-115.81, 37.24], "bbox": (-115.81, 37.24, -115.81, 37.24)},
            {"type": "LineString", "coordinates": [[8.919, 44.4074], [8.923, 44.4075]], "bbox": (8.919, 44.4074, 8.923, 44.4075)},
            {"type": "Polygon", "coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]],
                                                [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]],
                "bbox": (-120.43, -20.28, 23.194, 57.322)},
            {"type": "Point", "coordinates": [-155.52, 19.61], "bbox": (-155.52, 19.61, -155.52, 19.61)},
            {"type": "Point", "coordinates": [-156.22, 20.74], "bbox": (-156.22, 20.74, -156.22, 20.74)},
            {"type": "Point", "coordinates": [-157.97, 21.46], "bbox": (-157.97, 21.46, -157.97, 21.46)},
            {"type": "LineString", "coordinates": [[3.75, 9.25], [-130.95, 1.52]], "bbox": (-130.95, 1.52, 3.75, 9.25)},
            {"type": "LineString", "coordinates": [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]], "bbox": (-1.35, -34.25, 23.15, 77.95)},
            {"type": "Polygon", "coordinates": [[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], "bbox": (-130.91, 1.52, 35.12, 72.234)},
            {"type": "Polygon", "coordinates": [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]], "bbox": (-1.31, -34.29, 23.18, 77.91)}
        ),
    },
}

geometry_to_wkb_parameters = {
    0: {
        "geometry": POINT,
        "endian_big": True,
        "return_value": POINT_WKB_BIG_ENDIAN
    },
    1: {
        "geometry": LINESTRING,
        "endian_big": True,
        "return_value": LINESTRING_WKB_BIG_ENDIAN,
    },
    2: {
        "geometry": POLYGON,
        "endian_big": True,
        "return_value": POLYGON_WKB_BIG_ENDIAN,
    },
    3: {
        "geometry": MULTIPOINT,
        "endian_big": True,
        "return_value": MULTIPOINT_WKB_BIG_ENDIAN,
    },
    4: {
        "geometry": MULTILINESTRING,
        "endian_big": True,
        "return_value": MULTILINESTRING_WKB_BIG_ENDIAN,
    },
    5: {
        "geometry": MULTIPOLYGON,
        "endian_big": True,
        "return_value": MULTIPOLYGON_WKB_BIG_ENDIAN,
    },
    6: {
        "geometry": GEOMETRYCOLLECTION,
        "endian_big": True,
        "return_value": GEOMETRYCOLLECTION_WKB_BIG_ENDIAN,
    },
    7: {
        "geometry": POINT,
        "endian_big": False,
        "return_value": POINT_WKB_LITTLE_ENDIAN,
    },
    8: {
        "geometry": LINESTRING,
        "endian_big": False,
        "return_value": LINESTRING_WKB_LITTLE_ENDIAN,
    },
    9: {
        "geometry": POLYGON,
        "endian_big": False,
        "return_value": POLYGON_WKB_LITTLE_ENDIAN,
    },
    10: {
        "geometry": MULTIPOINT,
        "endian_big": False,
        "return_value": MULTIPOINT_WKB_LITTLE_ENDIAN,
    },
    11: {
        "geometry": MULTILINESTRING,
        "endian_big": False,
        "return_value": MULTILINESTRING_WKB_LITTLE_ENDIAN,
    },
    12: {
        "geometry": MULTIPOLYGON,
        "endian_big": False,
        "return_value": MULTIPOLYGON_WKB_LITTLE_ENDIAN,
    },
    13: {
        "geometry": GEOMETRYCOLLECTION,
        "endian_big": False,
        "return_value": GEOMETRYCOLLECTION_WKB_LITTLE_ENDIAN,
    },
    14: {
        "geometry": POINT_EMPTY,
        "endian_big": True,
        "return_value": POINT_EMPTY_WKB_BIG_ENDIAN,
    },
    15: {
        "geometry": LINESTRING_EMPTY,
        "endian_big": True,
        "return_value": LINESTRING_EMPTY_WKB_BIG_ENDIAN,
    },
    16: {
        "geometry": POLYGON_EMPTY,
        "endian_big": True,
        "return_value": POLYGON_EMPTY_WKB_BIG_ENDIAN,
    },
    17: {
        "geometry": MULTIPOINT_EMPTY,
        "endian_big": True,
        "return_value": MULTIPOINT_EMPTY_WKB_BIG_ENDIAN,
    },
    18: {
        "geometry": MULTILINESTRING_EMPTY,
        "endian_big": True,
        "return_value": MULTILINESTRING_EMPTY_WKB_BIG_ENDIAN,
    },
    19: {
        "geometry": MULTIPOLYGON_EMPTY,
        "endian_big": True,
        "return_value": MULTIPOLYGON_EMPTY_WKB_BIG_ENDIAN,
    },
    20: {
        "geometry": GEOMETRYCOLLECTION_EMPTY,
        "endian_big": True,
        "return_value": GEOMETRYCOLLECTION_EMPTY_WKB_BIG_ENDIAN,
    },
    21: {
        "geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
        "endian_big": True,
        "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_BIG_ENDIAN,
    },
    22: {
        "geometry": POINT_EMPTY,
        "endian_big": False,
        "return_value": POINT_EMPTY_WKB_LITTLE_ENDIAN,
    },
    23: {
        "geometry": LINESTRING_EMPTY,
        "endian_big": False,
        "return_value": LINESTRING_EMPTY_WKB_LITTLE_ENDIAN,
    },
    24: {
        "geometry": POLYGON_EMPTY,
        "endian_big": False,
        "return_value": POLYGON_EMPTY_WKB_LITTLE_ENDIAN,
    },
    25: {
        "geometry": MULTIPOINT_EMPTY,
        "endian_big": False,
        "return_value": MULTIPOINT_EMPTY_WKB_LITTLE_ENDIAN,
    },
    26: {
        "geometry": MULTILINESTRING_EMPTY,
        "endian_big": False,
        "return_value": MULTILINESTRING_EMPTY_WKB_LITTLE_ENDIAN,
    },
    27: {
        "geometry": MULTIPOLYGON_EMPTY,
        "endian_big": False,
        "return_value": MULTIPOLYGON_EMPTY_WKB_LITTLE_ENDIAN,
    },
    28: {
        "geometry": GEOMETRYCOLLECTION_EMPTY,
        "endian_big": False,
        "return_value": GEOMETRYCOLLECTION_EMPTY_WKB_LITTLE_ENDIAN,
    },
    29: {
        "geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
        "endian_big": False,
        "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_LITTLE_ENDIAN,
    },
}

wkb_to_geometry_parameters = {
    0: {
        "wkb_geometry": POINT_WKB_BIG_ENDIAN,
        "return_value": POINT,
        "bbox": False
    },
    1: {
        "wkb_geometry": LINESTRING_WKB_BIG_ENDIAN,
        "return_value": LINESTRING,
        "bbox": False
    },
    2: {
        "wkb_geometry": POLYGON_WKB_BIG_ENDIAN,
        "return_value": POLYGON,
        "bbox": False
    },
    3: {
        "wkb_geometry": MULTIPOINT_WKB_BIG_ENDIAN,
        "return_value": MULTIPOINT,
        "bbox": False
    },
    4: {
        "wkb_geometry": MULTILINESTRING_WKB_BIG_ENDIAN,
        "return_value": MULTILINESTRING,
        "bbox": False
    },
    5: {
        "wkb_geometry": MULTIPOLYGON_WKB_BIG_ENDIAN,
        "return_value": MULTIPOLYGON,
        "bbox": False
    },
    6: {
        "wkb_geometry": GEOMETRYCOLLECTION_WKB_LITTLE_ENDIAN,
        "return_value": GEOMETRYCOLLECTION,
        "bbox": False
    },
    7: {
        "wkb_geometry": POINT_WKB_LITTLE_ENDIAN,
        "return_value": POINT,
        "bbox": False
    },
    8: {
        "wkb_geometry": LINESTRING_WKB_LITTLE_ENDIAN,
        "return_value": LINESTRING,
        "bbox": False
    },
    9: {
        "wkb_geometry": POLYGON_WKB_LITTLE_ENDIAN,
        "return_value": POLYGON,
        "bbox": False
    },
    10: {
        "wkb_geometry": MULTIPOINT_WKB_LITTLE_ENDIAN,
        "return_value": MULTIPOINT,
        "bbox": False
    },
    11: {
        "wkb_geometry": MULTILINESTRING_WKB_LITTLE_ENDIAN,
        "return_value": MULTILINESTRING,
        "bbox": False
    },
    12: {
        "wkb_geometry": MULTIPOLYGON_WKB_LITTLE_ENDIAN,
        "return_value": MULTIPOLYGON,
        "bbox": False
    },
    13: {
        "wkb_geometry": GEOMETRYCOLLECTION_WKB_LITTLE_ENDIAN,
        "return_value": GEOMETRYCOLLECTION,
        "bbox": False
    },
    14: {
        "wkb_geometry": MULTIPOINT_WKB_VARYING_ENDIAN,
        "return_value": MULTIPOINT,
        "bbox": False
    },
    15: {
        "wkb_geometry": MULTILINESTRING_WKB_VARYING_ENDIAN,
        "return_value": MULTILINESTRING,
        "bbox": False
    },
    16: {
        "wkb_geometry": MULTIPOLYGON_WKB_VARYING_ENDIAN,
        "return_value": MULTIPOLYGON,
        "bbox": False
    },
    17: {
        "wkb_geometry": GEOMETRYCOLLECTION_WKB_VARYING_ENDIAN,
        "return_value": GEOMETRYCOLLECTION,
        "bbox": False
    },
    18: {
        "wkb_geometry": POINT_WKB_BIG_ENDIAN,
        "return_value": POINT_WITH_BBOX,
        "bbox": True
    },
    19: {
        "wkb_geometry": LINESTRING_WKB_BIG_ENDIAN,
        "return_value": LINESTRING_WITH_BBOX,
        "bbox": True
    },
    20: {
        "wkb_geometry": POLYGON_WKB_BIG_ENDIAN,
        "return_value": POLYGON_WITH_BBOX,
        "bbox": True
    },
    21: {
        "wkb_geometry": MULTIPOINT_WKB_BIG_ENDIAN,
        "return_value": MULTIPOINT_WITH_BBOX,
        "bbox": True
    },
    22: {
        "wkb_geometry": MULTILINESTRING_WKB_BIG_ENDIAN,
        "return_value": MULTILINESTRING_WITH_BBOX,
        "bbox": True
    },
    23: {
        "wkb_geometry": MULTIPOLYGON_WKB_BIG_ENDIAN,
        "return_value": MULTIPOLYGON_WITH_BBOX,
        "bbox": True
    },
    24: {
        "wkb_geometry": GEOMETRYCOLLECTION_WKB_LITTLE_ENDIAN,
        "return_value": GEOMETRYCOLLECTION_WITH_BBOX,
        "bbox": True
    },
    25: {
        "wkb_geometry": POINT_WKB_LITTLE_ENDIAN,
        "return_value": POINT_WITH_BBOX,
        "bbox": True
    },
    26: {
        "wkb_geometry": LINESTRING_WKB_LITTLE_ENDIAN,
        "return_value": LINESTRING_WITH_BBOX,
        "bbox": True
    },
    27: {
        "wkb_geometry": POLYGON_WKB_LITTLE_ENDIAN,
        "return_value": POLYGON_WITH_BBOX,
        "bbox": True
    },
    28: {
        "wkb_geometry": MULTIPOINT_WKB_LITTLE_ENDIAN,
        "return_value": MULTIPOINT_WITH_BBOX,
        "bbox": True
    },
    29: {
        "wkb_geometry": MULTILINESTRING_WKB_LITTLE_ENDIAN,
        "return_value": MULTILINESTRING_WITH_BBOX,
        "bbox": True
    },
    30: {
        "wkb_geometry": MULTIPOLYGON_WKB_LITTLE_ENDIAN,
        "return_value": MULTIPOLYGON_WITH_BBOX,
        "bbox": True
    },
    31: {
        "wkb_geometry": GEOMETRYCOLLECTION_WKB_LITTLE_ENDIAN,
        "return_value": GEOMETRYCOLLECTION_WITH_BBOX,
        "bbox": True
    },
    32: {
        "wkb_geometry": MULTIPOINT_WKB_VARYING_ENDIAN,
        "return_value": MULTIPOINT_WITH_BBOX,
        "bbox": True
    },
    33: {
        "wkb_geometry": MULTILINESTRING_WKB_VARYING_ENDIAN,
        "return_value": MULTILINESTRING_WITH_BBOX,
        "bbox": True
    },
    34: {
        "wkb_geometry": MULTIPOLYGON_WKB_VARYING_ENDIAN,
        "return_value": MULTIPOLYGON_WITH_BBOX,
        "bbox": True
    },
    35: {
        "wkb_geometry": GEOMETRYCOLLECTION_WKB_VARYING_ENDIAN,
        "return_value": GEOMETRYCOLLECTION_WITH_BBOX,
        "bbox": True
    },
    36: {
        "wkb_geometry": POINT_EMPTY_WKB_BIG_ENDIAN,
        "return_value": POINT_EMPTY,
        "bbox": True
    },
    37: {
        "wkb_geometry": POINT_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": POINT_EMPTY,
        "bbox": True
    },
    38: {
        "wkb_geometry": LINESTRING_EMPTY_WKB_BIG_ENDIAN,
        "return_value": LINESTRING_EMPTY,
        "bbox": True
    },
    39: {
        "wkb_geometry": LINESTRING_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": LINESTRING_EMPTY,
        "bbox": True
    },
    40: {
        "wkb_geometry": POLYGON_EMPTY_WKB_BIG_ENDIAN,
        "return_value": POLYGON_EMPTY,
        "bbox": True
    },
    41: {
        "wkb_geometry": POLYGON_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": POLYGON_EMPTY,
        "bbox": True
    },
    42: {
        "wkb_geometry": MULTIPOINT_EMPTY_WKB_BIG_ENDIAN ,
        "return_value": MULTIPOINT_EMPTY,
        "bbox": True
    },
    43: {
        "wkb_geometry": MULTIPOINT_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": MULTIPOINT_EMPTY,
        "bbox": True
    },
    44: {
        "wkb_geometry": MULTILINESTRING_EMPTY_WKB_BIG_ENDIAN,
        "return_value": MULTILINESTRING_EMPTY,
        "bbox": True
    },
    45: {
        "wkb_geometry": MULTILINESTRING_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": MULTILINESTRING_EMPTY,
        "bbox": True
    },
    46: {
        "wkb_geometry": MULTIPOLYGON_EMPTY_WKB_BIG_ENDIAN,
        "return_value": MULTIPOLYGON_EMPTY,
        "bbox": True
    },
    47: {
        "wkb_geometry": MULTIPOLYGON_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": MULTIPOLYGON_EMPTY,
        "bbox": True
    },
    48: {
        "wkb_geometry": GEOMETRYCOLLECTION_EMPTY_WKB_BIG_ENDIAN,
        "return_value": GEOMETRYCOLLECTION_EMPTY,
        "bbox": True
    },
    49: {
        "wkb_geometry": GEOMETRYCOLLECTION_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": GEOMETRYCOLLECTION_EMPTY,
        "bbox": True
    },
    50: {
        "wkb_geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_BIG_ENDIAN,
        "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WITH_BBOX,
        "bbox": True
    },
    51: {
        "wkb_geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_LITTLE_ENDIAN,
        "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WITH_BBOX,
        "bbox": True
    },
    52: {
        "wkb_geometry": POINT_EMPTY_WKB_BIG_ENDIAN,
        "return_value": POINT_EMPTY,
        "bbox": False
    },
    53: {
        "wkb_geometry": POINT_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": POINT_EMPTY,
        "bbox": False
    },
    54: {
        "wkb_geometry": LINESTRING_EMPTY_WKB_BIG_ENDIAN,
        "return_value": LINESTRING_EMPTY,
        "bbox": False
    },
    55: {
        "wkb_geometry": LINESTRING_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": LINESTRING_EMPTY,
        "bbox": False
    },
    56: {
        "wkb_geometry": POLYGON_EMPTY_WKB_BIG_ENDIAN,
        "return_value": POLYGON_EMPTY,
        "bbox": False
    },
    57: {
        "wkb_geometry": POLYGON_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": POLYGON_EMPTY,
        "bbox": False
    },
    58: {
        "wkb_geometry": MULTIPOINT_EMPTY_WKB_BIG_ENDIAN ,
        "return_value": MULTIPOINT_EMPTY,
        "bbox": False
    },
    59: {
        "wkb_geometry": MULTIPOINT_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": MULTIPOINT_EMPTY,
        "bbox": False
    },
    60: {
        "wkb_geometry": MULTILINESTRING_EMPTY_WKB_BIG_ENDIAN,
        "return_value": MULTILINESTRING_EMPTY,
        "bbox": False
    },
    61: {
        "wkb_geometry": MULTILINESTRING_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": MULTILINESTRING_EMPTY,
        "bbox": False
    },
    62: {
        "wkb_geometry": MULTIPOLYGON_EMPTY_WKB_BIG_ENDIAN,
        "return_value": MULTIPOLYGON_EMPTY,
        "bbox": False
    },
    63: {
        "wkb_geometry": MULTIPOLYGON_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": MULTIPOLYGON_EMPTY,
        "bbox": False
    },
    64: {
        "wkb_geometry": GEOMETRYCOLLECTION_EMPTY_WKB_BIG_ENDIAN,
        "return_value": GEOMETRYCOLLECTION_EMPTY,
        "bbox": False
    },
    65: {
        "wkb_geometry": GEOMETRYCOLLECTION_EMPTY_WKB_LITTLE_ENDIAN,
        "return_value": GEOMETRYCOLLECTION_EMPTY,
        "bbox": False
    },
    66: {
        "wkb_geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_BIG_ENDIAN,
        "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
        "bbox": False
    },
    67: {
        "wkb_geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKB_LITTLE_ENDIAN,
        "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
        "bbox": False
    },
}

geometry_to_wkt_parameters = {
    0: {
        "geometry": POINT,
        "return_value": POINT_WKT
    },
    1: {
        "geometry": LINESTRING,
        "return_value": LINESTRING_WKT
    },
    2: {
        "geometry": POLYGON,
        "return_value": POLYGON_WKT
    },
    3: {
        "geometry": MULTIPOINT,
        "return_value": MULTIPOINT_WKT
    },
    4: {
        "geometry": MULTILINESTRING,
        "return_value": MULTILINESTRING_WKT
    },
    5: {
        "geometry": MULTIPOLYGON,
        "return_value": MULTIPOLYGON_WKT
    },
    6: {
        "geometry": GEOMETRYCOLLECTION,
        "return_value": GEOMETRYCOLLECTION_WKT
    },
    7: {
        "geometry": POINT_EMPTY,
        "return_value": POINT_EMPTY_WKT
    },
    8: {
        "geometry": LINESTRING_EMPTY,
        "return_value": LINESTRING_EMPTY_WKT
    },
    9: {
        "geometry": POLYGON_EMPTY,
        "return_value": POLYGON_EMPTY_WKT
    },
    10: {
        "geometry": MULTIPOINT_EMPTY,
        "return_value": MULTIPOINT_EMPTY_WKT
    },
    11: {
        "geometry": MULTILINESTRING_EMPTY,
        "return_value": MULTILINESTRING_EMPTY_WKT
    },
    12: {
        "geometry": MULTIPOLYGON_EMPTY,
        "return_value": MULTIPOLYGON_EMPTY_WKT
    },
    13: {
        "geometry": GEOMETRYCOLLECTION_EMPTY,
        "return_value": GEOMETRYCOLLECTION_EMPTY_WKT
    },
    14: {
        "geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
        "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKT
    }
}

wkt_to_geometry_parameters = {
    0: {
        "wkt_geometry": POINT_WKT,
        "bbox": False,
        "return_value": POINT
    },
    1: {
        "wkt_geometry": LINESTRING_WKT,
        "bbox": False,
        "return_value": LINESTRING
    },
    2: {
        "wkt_geometry": POLYGON_WKT,
        "bbox": False,
        "return_value": POLYGON
    },
    3: {
        "wkt_geometry": MULTIPOINT_WKT,
        "bbox": False,
        "return_value": MULTIPOINT
     },
    4: {
        "wkt_geometry": MULTILINESTRING_WKT,
        "bbox": False,
        "return_value": MULTILINESTRING
    },
    5: {
        "wkt_geometry": MULTIPOLYGON_WKT,
        "bbox": False,
        "return_value": MULTIPOLYGON
    },
    6: {
        "wkt_geometry": GEOMETRYCOLLECTION_WKT,
        "bbox": False,
        "return_value": GEOMETRYCOLLECTION
    },
    7: {
        "wkt_geometry": POINT_WKT,
        "bbox": True,
        "return_value": POINT_WITH_BBOX
    },
    8: {
        "wkt_geometry": LINESTRING_WKT,
        "bbox": True,
        "return_value": LINESTRING_WITH_BBOX
    },
    9: {
        "wkt_geometry": POLYGON_WKT,
        "bbox": True,
        "return_value": POLYGON_WITH_BBOX
    },
    10: {
        "wkt_geometry": MULTIPOINT_WKT,
        "bbox": True,
        "return_value": MULTIPOINT_WITH_BBOX
    },
    11: {
        "wkt_geometry": MULTILINESTRING_WKT,
        "bbox": True,
        "return_value": MULTILINESTRING_WITH_BBOX
    },
    12: {
        "wkt_geometry": MULTIPOLYGON_WKT,
        "bbox": True,
        "return_value": MULTIPOLYGON_WITH_BBOX
    },
    13: {
        "wkt_geometry": GEOMETRYCOLLECTION_WKT,
        "bbox": True,
        "return_value": GEOMETRYCOLLECTION_WITH_BBOX
    },
    14: {
        "wkt_geometry": POINT_EMPTY_WKT,
        "bbox": False,
        "return_value": POINT_EMPTY
    },
    15: {
        "wkt_geometry": LINESTRING_EMPTY_WKT,
        "bbox": False,
        "return_value": LINESTRING_EMPTY
    },
    16: {
        "wkt_geometry": POLYGON_EMPTY_WKT,
        "bbox": False,
        "return_value": POLYGON_EMPTY
    },
    17: {
        "wkt_geometry": MULTIPOINT_EMPTY_WKT,
        "bbox": False,
        "return_value": MULTIPOINT_EMPTY
    },
    18: {
        "wkt_geometry": MULTILINESTRING_EMPTY_WKT,
        "bbox": False,
        "return_value": MULTILINESTRING_EMPTY
    },
    19: {
        "wkt_geometry": MULTIPOLYGON_EMPTY_WKT,
        "bbox": False,
        "return_value": MULTIPOLYGON_EMPTY
    },
    20: {
        "wkt_geometry": GEOMETRYCOLLECTION_EMPTY_WKT,
        "bbox": False,
        "return_value": GEOMETRYCOLLECTION_EMPTY
    },
    21: {
        "wkt_geometry": POINT_EMPTY_WKT,
        "bbox": True,
        "return_value": POINT_EMPTY
    },
    22: {
        "wkt_geometry": LINESTRING_EMPTY_WKT,
        "bbox": True,
        "return_value": LINESTRING_EMPTY
    },
    23: {
        "wkt_geometry": POLYGON_EMPTY_WKT,
        "bbox": True,
        "return_value": POLYGON_EMPTY
    },
    24: {
        "wkt_geometry": MULTIPOINT_EMPTY_WKT,
        "bbox": True,
        "return_value": MULTIPOINT_EMPTY
    },
    25: {
        "wkt_geometry": MULTILINESTRING_EMPTY_WKT,
        "bbox": True,
        "return_value": MULTILINESTRING_EMPTY
    },
    26: {
        "wkt_geometry": MULTIPOLYGON_EMPTY_WKT,
        "bbox": True,
        "return_value": MULTIPOLYGON_EMPTY
    },
    27: {
        "wkt_geometry": GEOMETRYCOLLECTION_EMPTY_WKT,
        "bbox": True,
        "return_value": GEOMETRYCOLLECTION_EMPTY
    },
    28: {
        "wkt_geometry": "GEOMETRYCOLLECTION (POINT EMPTY,LINESTRING (8.919 44.4074,8.923 44.4075),POLYGON ((2.38 57.322,23.194 -20.28,-120.43 19.15,2.38 57.322),(-5.21 23.51,15.21 -10.81,-20.51 1.51,-5.21 23.51)),MULTIPOINT (-155.52 19.61,-156.22 20.74,-157.97 21.46),MULTILINESTRING ((3.75 9.25,-130.95 1.52),(23.15 -34.25,-1.35 -4.65,3.45 77.95)),MULTIPOLYGON (((3.78 9.28,-130.91 1.52,35.12 72.234,3.78 9.28)),((23.18 -34.29,-1.31 -4.61,3.41 77.91,23.18 -34.29))))",
        "bbox": False,
        "return_value":  {"type": "GeometryCollection", "geometries": [{"type": "Point", "coordinates": []}, {"type": "LineString", "coordinates": [[8.919, 44.4074], [8.923, 44.4075]]}, {"type": "Polygon", "coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]]}, {"type": "MultiPoint", "coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]]}, {"type": "MultiLineString", "coordinates": [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]]}, {"type": "MultiPolygon", "coordinates": [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]]}]}
    },
    29: {
        "wkt_geometry": "GEOMETRYCOLLECTION (POINT EMPTY,LINESTRING (8.919 44.4074,8.923 44.4075),POLYGON ((2.38 57.322,23.194 -20.28,-120.43 19.15,2.38 57.322),(-5.21 23.51,15.21 -10.81,-20.51 1.51,-5.21 23.51)),MULTIPOINT (-155.52 19.61,-156.22 20.74,-157.97 21.46),MULTILINESTRING ((3.75 9.25,-130.95 1.52),(23.15 -34.25,-1.35 -4.65,3.45 77.95)),MULTIPOLYGON EMPTY)",
        "bbox": False,
        "return_value":  {"type": "GeometryCollection", "geometries": [{"type": "Point", "coordinates": []}, {"type": "LineString", "coordinates": [[8.919, 44.4074], [8.923, 44.4075]]}, {"type": "Polygon", "coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]]}, {"type": "MultiPoint", "coordinates": [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]]}, {"type": "MultiLineString", "coordinates": [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]]}, {"type": "MultiPolygon", "coordinates": []}]}
    },
    30: {
        "wkt_geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKT,
        "bbox": False,
        "return_value":  GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES
    },
    31: {
        "wkt_geometry": "GEOMETRYCOLLECTION (POINT EMPTY,LINESTRING (8.919 44.4074,8.923 44.4075),POLYGON ((2.38 57.322,23.194 -20.28,-120.43 19.15,2.38 57.322),(-5.21 23.51,15.21 -10.81,-20.51 1.51,-5.21 23.51)),MULTIPOINT (-155.52 19.61,-156.22 20.74,-157.97 21.46),MULTILINESTRING ((3.75 9.25,-130.95 1.52),(23.15 -34.25,-1.35 -4.65,3.45 77.95)),MULTIPOLYGON (((3.78 9.28,-130.91 1.52,35.12 72.234,3.78 9.28)),((23.18 -34.29,-1.31 -4.61,3.41 77.91,23.18 -34.29))))",
        "bbox": True,
        "return_value":  {'type': 'GeometryCollection', 'geometries': [{'type': 'Point', 'coordinates': []}, {'type': 'LineString', 'coordinates': [[8.919, 44.4074], [8.923, 44.4075]], 'bbox': (8.919, 44.4074, 8.923, 44.4075)}, {'type': 'Polygon', 'coordinates': [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]], 'bbox': (-120.43, -20.28, 23.194, 57.322)}, {'type': 'MultiPoint', 'coordinates': [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]], 'bbox': (-157.97, 19.61, -155.52, 21.46)}, {'type': 'MultiLineString', 'coordinates': [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]], 'bbox': (-130.95, -34.25, 23.15, 77.95)}, {'type': 'MultiPolygon', 'coordinates': [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]], [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]], 'bbox': (-130.91, -34.29, 35.12, 77.91)}], 'bbox': (-157.97, -34.29, 35.12, 77.95)}
    },
    32: {
        "wkt_geometry": "GEOMETRYCOLLECTION (POINT EMPTY,LINESTRING (8.919 44.4074,8.923 44.4075),POLYGON ((2.38 57.322,23.194 -20.28,-120.43 19.15,2.38 57.322),(-5.21 23.51,15.21 -10.81,-20.51 1.51,-5.21 23.51)),MULTIPOINT (-155.52 19.61,-156.22 20.74,-157.97 21.46),MULTILINESTRING ((3.75 9.25,-130.95 1.52),(23.15 -34.25,-1.35 -4.65,3.45 77.95)),MULTIPOLYGON EMPTY)",
        "bbox": True,
        "return_value":  {'type': 'GeometryCollection', 'geometries': [{'type': 'Point', 'coordinates': []}, {'type': 'LineString', 'coordinates': [[8.919, 44.4074], [8.923, 44.4075]], 'bbox': (8.919, 44.4074, 8.923, 44.4075)}, {'type': 'Polygon', 'coordinates': [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]], [[-5.21, 23.51], [15.21, -10.81], [-20.51, 1.51], [-5.21, 23.51]]], 'bbox': (-120.43, -20.28, 23.194, 57.322)}, {'type': 'MultiPoint', 'coordinates': [[-155.52, 19.61], [-156.22, 20.74], [-157.97, 21.46]], 'bbox': (-157.97, 19.61, -155.52, 21.46)}, {'type': 'MultiLineString', 'coordinates': [[[3.75, 9.25], [-130.95, 1.52]], [[23.15, -34.25], [-1.35, -4.65], [3.45, 77.95]]], 'bbox': (-130.95, -34.25, 23.15, 77.95)}, {'type': 'MultiPolygon', 'coordinates': []}], 'bbox': (-157.97, -34.25, 23.194, 77.95)}
    },
    33: {
        "wkt_geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKT,
        "bbox": True,
        "return_value":  GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WITH_BBOX
    },

}

force_rhr_parameters = {
    0: {
        "polygon_geometry": {'type': 'Polygon',
                             'coordinates': [[[0, 0], [5, 0], [0, 5], [0, 0]],
                                             [[1, 1], [1, 3], [3, 1], [1, 1]]]},
        "return_value": {'type': 'Polygon',
                         'coordinates': [[[0, 0], [0, 5], [5, 0], [0, 0]],
                                         [[1, 1], [3, 1], [1, 3], [1, 1]]]}
    },
    1: {
        "polygon_geometry": POLYGON,
        "return_value": {"type": "Polygon",
                         "coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]],
                                         [[-5.21, 23.51], [-20.51, 1.51], [15.21, -10.81], [-5.21, 23.51]]]}
    },
    2: {
        "polygon_geometry": MULTIPOLYGON,
        "return_value": {"type": "MultiPolygon",
                         "coordinates": [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]],
                                         [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]]}
    },
    3: {
        "polygon_geometry": POLYGON_WITH_BBOX,
        "return_value": {"type": "Polygon",
                         "coordinates": [[[2.38, 57.322], [23.194, -20.28], [-120.43, 19.15], [2.38, 57.322]],
                                         [[-5.21, 23.51], [-20.51, 1.51], [15.21, -10.81], [-5.21, 23.51]]],
                         'bbox': (-120.43, -20.28, 23.194, 57.322)}
    },
    4: {
        "polygon_geometry": MULTIPOLYGON_WITH_BBOX,
        "return_value": {"type": "MultiPolygon",
                         "coordinates": [[[[3.78, 9.28], [-130.91, 1.52], [35.12, 72.234], [3.78, 9.28]]],
                                         [[[23.18, -34.29], [-1.31, -4.61], [3.41, 77.91], [23.18, -34.29]]]],
                         'bbox': (-130.91, -34.29, 35.12, 77.91)}
    }
}

geometry_to_bbox_parameters = {
    0: {
        "geometry": POINT,
        "return_value": (-115.81, 37.24, -115.81, 37.24)
    },
    1: {
        "geometry": POINT_EMPTY,
        "return_value": ()
    },
    2: {
        "geometry": LINESTRING,
        "return_value": (8.919, 44.4074, 8.923, 44.4075)
    },
    3: {
        "geometry": LINESTRING_EMPTY,
        "return_value": ()
    },
    4: {
        "geometry": POLYGON,
        "return_value": (-120.43, -20.28, 23.194, 57.322)
    },
    5: {
        "geometry": POLYGON_EMPTY,
        "return_value": ()
    },
    6: {
        "geometry": MULTIPOINT,
        "return_value": (-157.97, 19.61, -155.52, 21.46)
    },
    7: {
        "geometry": MULTIPOINT_EMPTY,
        "return_value": ()
    },
    8: {
        "geometry": MULTILINESTRING,
        "return_value": (-130.95, -34.25, 23.15, 77.95)
    },
    9: {
        "geometry": MULTILINESTRING_EMPTY,
        "return_value": ()
    },
    10: {
        "geometry": MULTIPOLYGON,
        "return_value": (-130.91, -34.29, 35.12, 77.91)
    },
    11: {
        "geometry": MULTIPOLYGON_EMPTY,
        "return_value": ()
    },
    12: {
        "geometry": GEOMETRYCOLLECTION,
        "return_value": (-157.97, -34.29, 35.12, 77.95)
    },
    13: {
        "geometry": GEOMETRYCOLLECTION_EMPTY,
        "return_value": ()
    },
    14: {
        "geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
        "return_value": (-130.95, -34.25, 23.194, 77.95)
    },
}

reproject_geometry_parameters = {
    0: {
        "geometry": POINT_paris,
        "in_crs": 4326,
        "out_crs": 3857,
        "bbox_extent": False,
        "return_value": {'type': 'Point', 'coordinates': [5438327.16043688, 261547.21305842063]}
    },
    1: {
        "geometry": LINESTRING_loire,
        "in_crs": 4326,
        "out_crs": 3857,
        "bbox_extent": False,
        "return_value": {'type': 'LineString', 'coordinates': [[4991164.710956789, 470667.1894408509], [4990731.070264817, 443692.1861621149], [5005458.40922689, 431433.4687335367], [5029641.333699537, 436336.76222544693], [5061885.1824026825, 476185.82346659637], [5095243.898617723, 465762.0323583953], [5122482.00067491, 444305.1646159712], [5174072.289655546, 446757.1194601116], [5213943.2990773525, 387927.55995858513], [5257288.864360869, 329130.94465117675], [5292893.5352052, 319334.3595306902], [5331563.268140679, 199380.23371211483], [5297844.455963307, 151665.35499325398], [5276360.097425759, 77050.39851275018], [5253965.816465867, 11006.937536431236], [5274704.183458721, -35466.96390477308], [5274704.183458721, -106405.27875036073], [5254796.753796112, -174909.83978766855], [5265588.30151634, -225077.31171897362], [5263099.697664755, -243434.57931956137]]}
    },
    2: {
        "geometry": POLYGON_france,
        "in_crs": 4326,
        "out_crs": 3857,
        "bbox_extent": False,
        "return_value": {'type': 'Polygon', 'coordinates': [[[5691121.331408269, 274034.58011437685], [5663413.730299147, 190815.28053267428], [5579397.232129416, 190815.28053267428], [5541624.966001905, 44028.07795154968], [5513120.974059377, 4891.970289888127], [5494034.955297874, 39136.00405828938], [5481273.858178693, -122306.7402679829], [5528975.038124101, -141878.82380276656], [5528975.038124101, -200603.82743311874], [5481273.858178693, -176133.2953631094], [5410556.679537224, -151665.35499325386], [5394359.056275529, -288724.7765621929], [5429932.40990119, -337703.59228165745], [5417022.698635901, -514212.9714432467], [5381367.436017343, -528937.9820861171], [5384618.135468335, -489677.324284432], [5361824.1023497945, -470054.02966838237], [5352027.266309075, -514212.9714432467], [5312671.997546676, -484771.07413239026], [5342213.6432256345, -450435.1754383533], [5309380.257134417, -313211.8775221162], [5239821.993006453, -225077.31171897362], [5223138.929597878, -249554.10895371658], [5152558.877302665, -136985.68488510244], [5094817.35101598, -112521.14182904222], [5022741.306884777, -73381.16598105516], [5064028.910207735, -127199.64599861919], [4939355.674712992, -127199.64599861919], [4819377.013749287, -195709.49638131232], [4747789.842569971, 63596.66132119292], [4772930.491147904, 73381.16598105406], [4726167.793480721, 210392.8466856628], [4715331.539640287, 362200.28291744436], [4783676.994669552, 327906.3295569171], [4844255.608728921, 465148.90711679385], [4840707.143432099, 548575.7195347899], [4797979.466466913, 666517.6914199266], [4808686.665599899, 720647.9988647103], [4865507.052670565, 843870.086304386], [4907807.5156494025, 848805.1873340728], [4914831.344882991, 784687.1904980997], [5012377.196422563, 750195.1744573859], [5077731.417656916, 779758.3846682829], [5159316.38143989, 769902.1599116981], [5122057.328205316, 686195.7029567532], [5176177.348932982, 681275.5972836748], [5229817.769522452, 760047.7644609702], [5292893.5352052, 843870.086304386], [5348757.9241158655, 853740.7936106111], [5452452.813755994, 917951.0232172378], [5465280.734998899, 750195.1744573859], [5506766.38167384, 715724.9833843986], [5500404.376190229, 637012.463736638], [5566836.042832296, 514212.97144324664], [5635557.354791556, 323007.9895015968], [5691121.331408269, 274034.58011437685]]]}
    },
    3: {
        "geometry": MULTIPOINT_paris_tokyo,
        "in_crs": 4326,
        "out_crs": 3857,
        "bbox_extent": False,
        "return_value": {'type': 'MultiPoint', 'coordinates': [[5438327.160433801, 261547.21305793806], [float("inf"), float("inf")]]}
    },
    4: {
        "geometry": MULTILINESTRING_loire_katsuragawa_river,
        "in_crs": 4326,
        "out_crs": 3857,
        "bbox_extent": False,
        "return_value": {'type': 'MultiLineString', 'coordinates': [[[4991164.710956789, 470667.1894408509], [4990731.070264817, 443692.1861621149], [5005458.40922689, 431433.4687335367], [5029641.333699537, 436336.76222544693], [5061885.1824026825, 476185.82346659637], [5095243.898617723, 465762.0323583953], [5122482.00067491, 444305.1646159712], [5174072.289655546, 446757.1194601116], [5213943.2990773525, 387927.55995858513], [5257288.864360869, 329130.94465117675], [5292893.5352052, 319334.3595306902], [5331563.268140679, 199380.23371211483], [5297844.455963307, 151665.35499325398], [5276360.097425759, 77050.39851275018], [5253965.816465867, 11006.937536431236], [5274704.183458721, -35466.96390477308], [5274704.183458721, -106405.27875036073], [5254796.753796112, -174909.83978766855], [5265588.30151634, -225077.31171897362], [5263099.697664755, -243434.57931956137]], [[135.4222869873047, 34.68291096793206], [135.50262451171875, 34.722426197808446], [135.61248779296875, 34.78899484825181], [135.68389892578125, 34.88705743313571], [135.73471069335938, 34.92422301690581], [135.73780059814453, 34.941392337729816], [135.70758819580078, 34.998222460984685], [135.69110870361328, 34.998222460984685], [135.6540298461914, 35.02999636902566], [135.57952880859375, 35.02212433874883], [135.54905891418457, 35.05262423302113], [135.51189422607422, 35.09266439952991], [135.51695823669434, 35.11653865167172], [135.49266815185547, 35.12917513034949], [135.5076026916504, 35.15121407216851], [135.51644325256348, 35.15345974393076], [135.51738739013672, 35.14665236059329], [135.53704261779782, 35.14430122477116], [135.54309368133545, 35.13215845728398], [135.56824207305908, 35.12829766045064], [135.57761907577515, 35.1388617696448], [135.5717396736145, 35.145582075842604], [135.58399200439453, 35.14419594844418], [135.60270309448242, 35.13844063537838], [135.60956954956055, 35.13212335995541], [135.6378936767578, 35.13984440779405], [135.63274383544922, 35.1540913279465], [135.64982414245605, 35.1707914371233], [135.6748867034912, 35.18664634969633], [135.68166732788086, 35.19667684282583], [135.70218086242676, 35.19836016087243], [135.70956230163574, 35.193029534057615], [135.7118797302246, 35.20256830337077], [135.71685791015625, 35.2116150714062], [135.72526931762695, 35.20130588351442], [135.736083984375, 35.21035279218927], [135.7476282119751, 35.20383070360394], [135.75419425964355, 35.20873985129727], [135.75912952423096, 35.201831894172635], [135.76183319091797, 35.20453202858757], [135.77406406402588, 35.20558400470673], [135.7796859741211, 35.221993067538584], [135.77805519104004, 35.23573485795656]]]}
    },
    5: {
        "geometry": MULTIPOLYGON_france_japan,
        "in_crs": 4326,
        "out_crs": 3857,
        "bbox_extent": False,
        "return_value": {'type': 'MultiPolygon', 'coordinates': [[[[5691121.331408269, 274034.58011437685], [5663413.730299147, 190815.28053267428], [5579397.232129416, 190815.28053267428], [5541624.966001905, 44028.07795154968], [5513120.974059377, 4891.970289888127], [5494034.955297874, 39136.00405828938], [5481273.858178693, -122306.7402679829], [5528975.038124101, -141878.82380276656], [5528975.038124101, -200603.82743311874], [5481273.858178693, -176133.2953631094], [5410556.679537224, -151665.35499325386], [5394359.056275529, -288724.7765621929], [5429932.40990119, -337703.59228165745], [5417022.698635901, -514212.9714432467], [5381367.436017343, -528937.9820861171], [5384618.135468335, -489677.324284432], [5361824.1023497945, -470054.02966838237], [5352027.266309075, -514212.9714432467], [5312671.997546676, -484771.07413239026], [5342213.6432256345, -450435.1754383533], [5309380.257134417, -313211.8775221162], [5239821.993006453, -225077.31171897362], [5223138.929597878, -249554.10895371658], [5152558.877302665, -136985.68488510244], [5094817.35101598, -112521.14182904222], [5022741.306884777, -73381.16598105516], [5064028.910207735, -127199.64599861919], [4939355.674712992, -127199.64599861919], [4819377.013749287, -195709.49638131232], [4747789.842569971, 63596.66132119292], [4772930.491147904, 73381.16598105406], [4726167.793480721, 210392.8466856628], [4715331.539640287, 362200.28291744436], [4783676.994669552, 327906.3295569171], [4844255.608728921, 465148.90711679385], [4840707.143432099, 548575.7195347899], [4797979.466466913, 666517.6914199266], [4808686.665599899, 720647.9988647103], [4865507.052670565, 843870.086304386], [4907807.5156494025, 848805.1873340728], [4914831.344882991, 784687.1904980997], [5012377.196422563, 750195.1744573859], [5077731.417656916, 779758.3846682829], [5159316.38143989, 769902.1599116981], [5122057.328205316, 686195.7029567532], [5176177.348932982, 681275.5972836748], [5229817.769522452, 760047.7644609702], [5292893.5352052, 843870.086304386], [5348757.9241158655, 853740.7936106111], [5452452.813755994, 917951.0232172378], [5465280.734998899, 750195.1744573859], [5506766.38167384, 715724.9833843986], [5500404.376190229, 637012.463736638], [5566836.042832296, 514212.97144324664], [5635557.354791556, 323007.9895015968], [5691121.331408269, 274034.58011437685]]], [[[140.888671875, 41.52502957323801], [139.910888671875, 40.65563874006118], [140.042724609375, 39.45316112807394], [139.658203125, 38.58252615935333], [138.80126953125, 37.80544394934271], [137.26318359375, 36.73888412439431], [136.91162109374997, 37.055177106660814], [137.39501953124997, 37.47485808497102], [136.669921875, 37.38761749978395], [136.77978515625, 36.77409249464195], [135.90087890625, 35.97800618085566], [136.03271484375, 35.639441068973944], [135.46142578124997, 35.460669951495305], [135.2197265625, 35.8356283888737], [133.4619140625, 35.47856499535729], [133.1982421875, 35.585851593232356], [132.626953125, 35.47856499535729], [132.71484375, 35.22767235493586], [131.396484375, 34.43409789359469], [130.869140625, 34.34343606848294], [131.02294921875, 33.96158628979907], [131.7041015625, 34.05265942137599], [132.34130859375, 33.815666308702774], [132.34130859375, 34.415973384481866], [132.71484375, 34.288991865037524], [133.3740234375, 34.43409789359469], [133.857421875, 34.361576287484176], [134.47265625, 34.75966612466248], [135.0, 34.66935854524543], [135.3955078125, 34.75966612466248], [135.24169921875, 34.34343606848294], [135.63720703125, 33.44977658311846], [136.38427734375, 34.17999758688084], [136.86767578125, 34.470335121217474], [136.69189453125, 35.137879119634185], [137.48291015625, 34.66935854524543], [138.14208984375, 34.687427949314845], [138.88916015625, 35.22767235493586], [138.71337890625, 34.65128519895413], [139.19677734375, 34.994003757575776], [139.482421875, 35.35321610123823], [139.89990234375, 35.69299463209881], [140.18554687499997, 35.567980458012094], [139.8779296875, 35.209721645221386], [139.85595703125, 34.939985151560435], [140.44921875, 35.22767235493586], [140.537109375, 35.65729624809628], [140.8447265625, 35.746512259918504], [140.44921875, 36.20882309283712], [140.80078125, 36.94989178681327], [140.9326171875, 38.09998264736481], [141.17431640625, 38.47939467327645], [141.591796875, 38.35888785866677], [141.591796875, 38.95940879245423], [142.03125, 39.58875727696545], [141.7236328125, 40.463666324587685], [141.43798828125, 40.697299008636755], [141.4599609375, 41.45919537950706], [141.21826171875, 41.29431726315258], [140.888671875, 41.52502957323801]]], [[[141.8994140625, 45.460130637921004], [141.4599609375, 43.54854811091286], [140.712890625, 43.54854811091286], [140.5810546875, 42.97250158602597], [139.921875, 42.32606244456202], [140.0537109375, 41.21172151054787], [141.064453125, 41.73852846935917], [140.44921875, 42.32606244456202], [140.66894531249997, 42.61779143282346], [141.767578125, 42.65012181368022], [143.525390625, 41.934976500546604], [145.4150390625, 43.26120612479979], [145.283203125, 44.402391829093915], [143.3935546875, 44.24519901522129], [141.8994140625, 45.460130637921004]]], [[[134.1265869140625, 34.34343606848294], [133.8629150390625, 34.35704160076073], [133.670654296875, 34.20271636159618], [133.5552978515625, 33.99347299511967], [133.0938720703125, 33.89321737944089], [132.95104980468747, 34.11180455556899], [132.791748046875, 33.99347299511967], [132.681884765625, 33.77458136371689], [132.0391845703125, 33.367237465838315], [132.38525390625, 33.463525475613785], [132.36328125, 33.31216783738619], [132.5335693359375, 33.27543541298162], [132.5225830078125, 33.16054697509142], [132.5665283203125, 32.92109653816924], [132.6983642578125, 32.94875863715422], [132.6324462890625, 32.76880048488168], [132.8466796875, 32.778037985363675], [133.00048828125, 32.7503226078097], [133.011474609375, 33.04090311724091], [133.2806396484375, 33.243281858479484], [133.253173828125, 33.4039312002347], [133.7091064453125, 33.53681606773302], [134.000244140625, 33.445193134508465], [134.18701171875, 33.23409295522519], [134.36279296875, 33.62376800118811], [134.769287109375, 33.83848275599514], [134.5770263671875, 34.093610452768715], [134.615478515625, 34.21180215769026], [134.1265869140625, 34.34343606848294]]], [[[131.0009765625, 33.96500329452545], [130.8966064453125, 33.890367484132945], [130.5010986328125, 33.87497640410958], [130.308837890625, 33.57343808567733], [129.96826171875, 33.454359789517014], [129.8858642578125, 33.568861182555565], [129.84741210937497, 33.30757713015298], [129.4573974609375, 33.35347332342168], [129.3310546875, 33.137551192346145], [129.56726074218747, 33.23868752757414], [129.6551513671875, 33.054716488042736], [129.83642578125, 32.704111144407406], [129.7869873046875, 32.55607364492026], [130.1385498046875, 32.791892438123696], [130.155029296875, 32.69486597787505], [130.2703857421875, 32.60698915452777], [130.3253173828125, 32.92109653816924], [130.220947265625, 33.18813395605041], [130.6494140625, 32.7872745269555], [130.3692626953125, 32.523657815699146], [130.0286865234375, 32.46806060917602], [129.9957275390625, 32.189559980413584], [130.220947265625, 32.35212281198644], [130.62744140624997, 32.61161640317033], [130.341796875, 32.143059999988445], [130.1715087890625, 32.189559980413584], [130.1220703125, 32.10584293285769], [130.4296875, 31.541089879585808], [130.25390625, 31.39115752282472], [130.67138671875, 31.16580958786196], [130.693359375, 31.55981453201843], [130.869140625, 31.147006308556566], [131.0888671875, 31.44741029142872], [131.3525390625, 31.42866311735861], [131.7041015625, 32.43561304116276], [131.923828125, 32.97180377635759], [131.46240234375, 33.37641235124676], [131.81396484375, 33.50475906922609], [131.63818359375, 33.65120829920497], [131.1767578125, 33.52307880890422], [131.0009765625, 33.96500329452545]]]]}
    },
    6: {
        "geometry": GEOMETRYCOLLECTION_paris_tokyo_loire_katsuragawa_river_france_japan,
        "in_crs": 4326,
        "out_crs": 3857,
        "bbox_extent": False,
        "return_value": {'type': 'GeometryCollection', 'geometries': [{'type': 'MultiPoint', 'coordinates': [[5438327.16043688, 261547.21305842063], [float("inf"), float("inf")]]}, {'type': 'MultiLineString', 'coordinates': [[[4.2242431640625, 44.83639545410477], [3.9825439453125, 44.83249999349062], [3.8726806640625, 44.96479793033101], [3.9166259765625, 45.182036837015886], [4.273681640625, 45.471688258104614], [4.1802978515625, 45.77135470445038], [3.9880371093749996, 46.01603873833416], [4.010009765624999, 46.479482189368646], [3.482666015625, 46.837649560937464], [2.955322265625, 47.2270293988673], [2.867431640625, 47.54687159892238], [1.7907714843749998, 47.89424772020999], [1.3623046875, 47.5913464767971], [0.6921386718749999, 47.39834920035926], [0.098876953125, 47.19717795172789], [-0.318603515625, 47.3834738721015], [-0.9558105468749999, 47.3834738721015], [-1.571044921875, 47.204642388766935], [-2.021484375, 47.301584511330795], [-2.186279296875, 47.27922900257082]], [[135.4222869873047, 34.68291096793206], [135.50262451171875, 34.722426197808446], [135.61248779296875, 34.78899484825181], [135.68389892578125, 34.88705743313571], [135.73471069335938, 34.92422301690581], [135.73780059814453, 34.941392337729816], [135.70758819580078, 34.998222460984685], [135.69110870361328, 34.998222460984685], [135.6540298461914, 35.02999636902566], [135.57952880859375, 35.02212433874883], [135.54905891418457, 35.05262423302113], [135.51189422607422, 35.09266439952991], [135.51695823669434, 35.11653865167172], [135.49266815185547, 35.12917513034949], [135.5076026916504, 35.15121407216851], [135.51644325256348, 35.15345974393076], [135.51738739013672, 35.14665236059329], [135.53704261779782, 35.14430122477116], [135.54309368133545, 35.13215845728398], [135.56824207305908, 35.12829766045064], [135.57761907577515, 35.1388617696448], [135.5717396736145, 35.145582075842604], [135.58399200439453, 35.14419594844418], [135.60270309448242, 35.13844063537838], [135.60956954956055, 35.13212335995541], [135.6378936767578, 35.13984440779405], [135.63274383544922, 35.1540913279465], [135.64982414245605, 35.1707914371233], [135.6748867034912, 35.18664634969633], [135.68166732788086, 35.19667684282583], [135.70218086242676, 35.19836016087243], [135.70956230163574, 35.193029534057615], [135.7118797302246, 35.20256830337077], [135.71685791015625, 35.2116150714062], [135.72526931762695, 35.20130588351442], [135.736083984375, 35.21035279218927], [135.7476282119751, 35.20383070360394], [135.75419425964355, 35.20873985129727], [135.75912952423096, 35.201831894172635], [135.76183319091797, 35.20453202858757], [135.77406406402588, 35.20558400470673], [135.7796859741211, 35.221993067538584], [135.77805519104004, 35.23573485795656]]]}, {'type': 'MultiPolygon', 'coordinates': [[[[2.4609375, 51.12421275782688], [1.7138671875, 50.875311142200765], [1.7138671875, 50.12057809796008], [0.3955078125, 49.781264058178344], [0.0439453125, 49.52520834197442], [0.3515625, 49.35375571830993], [-1.0986328125, 49.23912083246698], [-1.2744140625, 49.66762782262194], [-1.8017578124999998, 49.66762782262194], [-1.58203125, 49.23912083246698], [-1.3623046875, 48.60385760823255], [-2.5927734375, 48.45835188280866], [-3.0322265625, 48.777912755501845], [-4.6142578125, 48.66194284607006], [-4.74609375, 48.3416461723746], [-4.39453125, 48.37084770238366], [-4.21875, 48.16608541901253], [-4.6142578125, 48.07807894349862], [-4.350585937499999, 47.724544549099676], [-4.04296875, 47.989921667414194], [-2.8125, 47.69497434186282], [-2.021484375, 47.07012182383309], [-2.2412109375, 46.92025531537451], [-1.23046875, 46.28622391806706], [-1.0107421875, 45.767522962149876], [-0.6591796875, 45.120052841530544], [-1.142578125, 45.49094569262732], [-1.142578125, 44.37098696297173], [-1.7578125, 43.29320031385282], [0.5712890625, 42.65012181368022], [0.6591796875, 42.87596410238256], [1.8896484375, 42.45588764197166], [3.251953125, 42.35854391749705], [2.9443359375, 42.97250158602597], [4.1748046875, 43.51668853502906], [4.921875, 43.48481212891603], [5.9765625, 43.100982876188546], [6.459960937499999, 43.197167282501276], [7.55859375, 43.70759350405294], [7.6025390625, 44.08758502824516], [7.03125, 44.15068115978094], [6.723632812499999, 45.02695045318546], [6.9873046875, 45.61403741135093], [6.8994140625, 46.34692761055676], [6.15234375, 46.01222384063236], [6.1083984375, 46.49839225859763], [6.8115234375, 46.98025235521883], [7.55859375, 47.54687159892238], [7.646484374999999, 48.04870994288686], [8.2177734375, 48.980216985374994], [6.723632812499999, 49.095452162534826], [6.416015625, 49.468124067331644], [5.712890625, 49.410973199695846], [4.6142578125, 50.00773901463687], [2.900390625, 50.62507306341435], [2.4609375, 51.12421275782688]]], [[[140.888671875, 41.52502957323801], [139.910888671875, 40.65563874006118], [140.042724609375, 39.45316112807394], [139.658203125, 38.58252615935333], [138.80126953125, 37.80544394934271], [137.26318359375, 36.73888412439431], [136.91162109374997, 37.055177106660814], [137.39501953124997, 37.47485808497102], [136.669921875, 37.38761749978395], [136.77978515625, 36.77409249464195], [135.90087890625, 35.97800618085566], [136.03271484375, 35.639441068973944], [135.46142578124997, 35.460669951495305], [135.2197265625, 35.8356283888737], [133.4619140625, 35.47856499535729], [133.1982421875, 35.585851593232356], [132.626953125, 35.47856499535729], [132.71484375, 35.22767235493586], [131.396484375, 34.43409789359469], [130.869140625, 34.34343606848294], [131.02294921875, 33.96158628979907], [131.7041015625, 34.05265942137599], [132.34130859375, 33.815666308702774], [132.34130859375, 34.415973384481866], [132.71484375, 34.288991865037524], [133.3740234375, 34.43409789359469], [133.857421875, 34.361576287484176], [134.47265625, 34.75966612466248], [135.0, 34.66935854524543], [135.3955078125, 34.75966612466248], [135.24169921875, 34.34343606848294], [135.63720703125, 33.44977658311846], [136.38427734375, 34.17999758688084], [136.86767578125, 34.470335121217474], [136.69189453125, 35.137879119634185], [137.48291015625, 34.66935854524543], [138.14208984375, 34.687427949314845], [138.88916015625, 35.22767235493586], [138.71337890625, 34.65128519895413], [139.19677734375, 34.994003757575776], [139.482421875, 35.35321610123823], [139.89990234375, 35.69299463209881], [140.18554687499997, 35.567980458012094], [139.8779296875, 35.209721645221386], [139.85595703125, 34.939985151560435], [140.44921875, 35.22767235493586], [140.537109375, 35.65729624809628], [140.8447265625, 35.746512259918504], [140.44921875, 36.20882309283712], [140.80078125, 36.94989178681327], [140.9326171875, 38.09998264736481], [141.17431640625, 38.47939467327645], [141.591796875, 38.35888785866677], [141.591796875, 38.95940879245423], [142.03125, 39.58875727696545], [141.7236328125, 40.463666324587685], [141.43798828125, 40.697299008636755], [141.4599609375, 41.45919537950706], [141.21826171875, 41.29431726315258], [140.888671875, 41.52502957323801]]], [[[141.8994140625, 45.460130637921004], [141.4599609375, 43.54854811091286], [140.712890625, 43.54854811091286], [140.5810546875, 42.97250158602597], [139.921875, 42.32606244456202], [140.0537109375, 41.21172151054787], [141.064453125, 41.73852846935917], [140.44921875, 42.32606244456202], [140.66894531249997, 42.61779143282346], [141.767578125, 42.65012181368022], [143.525390625, 41.934976500546604], [145.4150390625, 43.26120612479979], [145.283203125, 44.402391829093915], [143.3935546875, 44.24519901522129], [141.8994140625, 45.460130637921004]]], [[[134.1265869140625, 34.34343606848294], [133.8629150390625, 34.35704160076073], [133.670654296875, 34.20271636159618], [133.5552978515625, 33.99347299511967], [133.0938720703125, 33.89321737944089], [132.95104980468747, 34.11180455556899], [132.791748046875, 33.99347299511967], [132.681884765625, 33.77458136371689], [132.0391845703125, 33.367237465838315], [132.38525390625, 33.463525475613785], [132.36328125, 33.31216783738619], [132.5335693359375, 33.27543541298162], [132.5225830078125, 33.16054697509142], [132.5665283203125, 32.92109653816924], [132.6983642578125, 32.94875863715422], [132.6324462890625, 32.76880048488168], [132.8466796875, 32.778037985363675], [133.00048828125, 32.7503226078097], [133.011474609375, 33.04090311724091], [133.2806396484375, 33.243281858479484], [133.253173828125, 33.4039312002347], [133.7091064453125, 33.53681606773302], [134.000244140625, 33.445193134508465], [134.18701171875, 33.23409295522519], [134.36279296875, 33.62376800118811], [134.769287109375, 33.83848275599514], [134.5770263671875, 34.093610452768715], [134.615478515625, 34.21180215769026], [134.1265869140625, 34.34343606848294]]], [[[131.0009765625, 33.96500329452545], [130.8966064453125, 33.890367484132945], [130.5010986328125, 33.87497640410958], [130.308837890625, 33.57343808567733], [129.96826171875, 33.454359789517014], [129.8858642578125, 33.568861182555565], [129.84741210937497, 33.30757713015298], [129.4573974609375, 33.35347332342168], [129.3310546875, 33.137551192346145], [129.56726074218747, 33.23868752757414], [129.6551513671875, 33.054716488042736], [129.83642578125, 32.704111144407406], [129.7869873046875, 32.55607364492026], [130.1385498046875, 32.791892438123696], [130.155029296875, 32.69486597787505], [130.2703857421875, 32.60698915452777], [130.3253173828125, 32.92109653816924], [130.220947265625, 33.18813395605041], [130.6494140625, 32.7872745269555], [130.3692626953125, 32.523657815699146], [130.0286865234375, 32.46806060917602], [129.9957275390625, 32.189559980413584], [130.220947265625, 32.35212281198644], [130.62744140624997, 32.61161640317033], [130.341796875, 32.143059999988445], [130.1715087890625, 32.189559980413584], [130.1220703125, 32.10584293285769], [130.4296875, 31.541089879585808], [130.25390625, 31.39115752282472], [130.67138671875, 31.16580958786196], [130.693359375, 31.55981453201843], [130.869140625, 31.147006308556566], [131.0888671875, 31.44741029142872], [131.3525390625, 31.42866311735861], [131.7041015625, 32.43561304116276], [131.923828125, 32.97180377635759], [131.46240234375, 33.37641235124676], [131.81396484375, 33.50475906922609], [131.63818359375, 33.65120829920497], [131.1767578125, 33.52307880890422], [131.0009765625, 33.96500329452545]]]]}]}
    }
}

if test_dependencies()['ogr']:
    geometry_to_ogr_geometry_parameters = {
        0: {
            "geometry": POINT,
            "return_value": ogr.CreateGeometryFromJson(str(POINT))
        },
        1: {
            "geometry": POINT_WITH_BBOX,
            "return_value": ogr.CreateGeometryFromJson(str(POINT))
        },
        2: {
            "geometry": POINT_EMPTY,
            "return_value": ogr.CreateGeometryFromWkt(POINT_EMPTY_WKT)
        },
        3: {
            "geometry": LINESTRING,
            "return_value": ogr.CreateGeometryFromJson(str(LINESTRING))
        },
        4: {
            "geometry": LINESTRING_WITH_BBOX,
            "return_value": ogr.CreateGeometryFromJson(str(LINESTRING))
        },
        5: {
            "geometry": LINESTRING_EMPTY,
            "return_value": ogr.CreateGeometryFromWkt(LINESTRING_EMPTY_WKT)
        },
        6: {
            "geometry": POLYGON,
            "return_value": ogr.CreateGeometryFromJson(str(POLYGON))
        },
        7: {
            "geometry": POLYGON_WITH_BBOX,
            "return_value": ogr.CreateGeometryFromJson(str(POLYGON))
        },
        8: {
            "geometry": POLYGON_EMPTY,
            "return_value": ogr.CreateGeometryFromWkt(POLYGON_EMPTY_WKT)
        },
        9: {
            "geometry": MULTIPOINT,
            "return_value": ogr.CreateGeometryFromJson(str(MULTIPOINT))
        },
        10: {
            "geometry": MULTIPOINT_WITH_BBOX,
            "return_value": ogr.CreateGeometryFromJson(str(MULTIPOINT))
        },
        11: {
            "geometry": MULTIPOINT_EMPTY,
            "return_value": ogr.CreateGeometryFromWkt(MULTIPOINT_EMPTY_WKT)
        },
        12: {
            "geometry": MULTILINESTRING,
            "return_value": ogr.CreateGeometryFromJson(str(MULTILINESTRING))
        },
        13: {
            "geometry": MULTILINESTRING_WITH_BBOX,
            "return_value": ogr.CreateGeometryFromJson(str(MULTILINESTRING))
        },
        14: {
            "geometry": MULTILINESTRING_EMPTY,
            "return_value": ogr.CreateGeometryFromWkt(MULTILINESTRING_EMPTY_WKT)
        },
        15: {
            "geometry": MULTIPOLYGON,
            "return_value": ogr.CreateGeometryFromJson(str(MULTIPOLYGON))
        },
        16: {
            "geometry": MULTIPOLYGON_WITH_BBOX,
            "return_value": ogr.CreateGeometryFromJson(str(MULTIPOLYGON))
        },
        17: {
            "geometry": MULTIPOLYGON_EMPTY,
            "return_value": ogr.CreateGeometryFromWkt(MULTIPOLYGON_EMPTY_WKT)
        },
        18: {
            "geometry": GEOMETRYCOLLECTION,
            "return_value": ogr.CreateGeometryFromJson(str(GEOMETRYCOLLECTION))
        },
        19: {
            "geometry": GEOMETRYCOLLECTION_WITH_BBOX,
            "return_value": ogr.CreateGeometryFromJson(str(GEOMETRYCOLLECTION))
        },
        20: {
            "geometry": GEOMETRYCOLLECTION_EMPTY,
            "return_value": ogr.CreateGeometryFromWkt(GEOMETRYCOLLECTION_EMPTY_WKT)
        },
        21: {
            "geometry": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
            "return_value": ogr.CreateGeometryFromWkt(GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKT)
        },
    }


    ogr_geometry_to_geometry_parameters = {
        0: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(POINT)),
            "bbox": False,
            "return_value": POINT,
        },
        1: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(POINT)),
            "bbox": True,
            "return_value": POINT_WITH_BBOX,
        },
        2: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(POINT_EMPTY_WKT),
            "bbox": True,
            "return_value": POINT_EMPTY,
        },
        3: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(LINESTRING)),
            "bbox": False,
            "return_value": LINESTRING,
        },
        4: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(LINESTRING)),
            "bbox": True,
            "return_value": LINESTRING_WITH_BBOX,
        },
        5: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(LINESTRING_EMPTY_WKT),
            "bbox": False,
            "return_value": LINESTRING_EMPTY,
        },
        6: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(POLYGON)),
            "bbox": False,
            "return_value": POLYGON,
        },
        7: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(POLYGON)),
            "bbox": True,
            "return_value": POLYGON_WITH_BBOX,
        },
        8: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(POLYGON_EMPTY_WKT),
            "bbox": True,
            "return_value": POLYGON_EMPTY,
        },
        9: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(MULTIPOINT)),
            "bbox": False,
            "return_value": MULTIPOINT,
        },
        10: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(MULTIPOINT)),
            "bbox": True,
            "return_value": MULTIPOINT_WITH_BBOX,
        },
        11: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(MULTIPOINT_EMPTY_WKT),
            "bbox": False,
            "return_value": MULTIPOINT_EMPTY,
        },
        12: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(MULTILINESTRING)),
            "bbox": False,
            "return_value": MULTILINESTRING,
        },
        13: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(MULTILINESTRING)),
            "bbox": True,
            "return_value": MULTILINESTRING_WITH_BBOX,
        },
        14: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(MULTILINESTRING_EMPTY_WKT),
            "bbox": True,
            "return_value": MULTILINESTRING_EMPTY,
        },
        15: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(MULTIPOLYGON)),
            "bbox": False,
            "return_value": MULTIPOLYGON,
        },
        16: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(MULTIPOLYGON)),
            "bbox": True,
            "return_value": MULTIPOLYGON_WITH_BBOX,
        },
        17: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(MULTIPOLYGON_EMPTY_WKT),
            "bbox": True,
            "return_value": MULTIPOLYGON_EMPTY,
        },
        18: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(GEOMETRYCOLLECTION)),
            "bbox": False,
            "return_value": GEOMETRYCOLLECTION,
        },
        19: {
            "ogr_geometry": ogr.CreateGeometryFromJson(str(GEOMETRYCOLLECTION)),
            "bbox": True,
            "return_value": GEOMETRYCOLLECTION_WITH_BBOX,
        },
        20: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(GEOMETRYCOLLECTION_EMPTY_WKT),
            "bbox": True,
            "return_value": GEOMETRYCOLLECTION_EMPTY,
        },
        21: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKT),
            "bbox": False,
            "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES,
        },
        22: {
            "ogr_geometry": ogr.CreateGeometryFromWkt(GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WKT),
            "bbox": True,
            "return_value": GEOMETRY_COLLECTION_WITH_EMPTY_GEOMETRIES_WITH_BBOX,
        },
    }


def test_all():

    # geometry_type_to_2d_geometry_type
    print(test_function(geometry_type_to_2d_geometry_type, geometry_type_to_2d_geometry_type_parameters))

    # geometry_to_2d_geometry
    print(test_function(geometry_to_2d_geometry, geometry_to_2d_geometry_parameters))

    # geometry_to_geometry_collection
    print(test_function(geometry_to_geometry_collection, geometry_to_geometry_collection_parameters))

    # multi_geometry_to_single_geometry
    print(test_function(multi_geometry_to_single_geometry, multi_geometry_to_single_geometry_parameters))

    # single_geometry_to_multi_geometry
    print(test_function(single_geometry_to_multi_geometry, single_geometry_to_multi_geometry_parameters))

    # geometry_to_multi_geometry
    print(test_function(geometry_to_multi_geometry, geometry_to_multi_geometry_parameters))

    # geometry_to_wkb
    print(test_function(geometry_to_wkb, geometry_to_wkb_parameters))

    # wkb_to_geometry
    print(test_function(wkb_to_geometry, wkb_to_geometry_parameters))

    # geometry_to_wkt
    print(test_function(geometry_to_wkt, geometry_to_wkt_parameters))

    # wkt_to_geometry
    print(test_function(wkt_to_geometry, wkt_to_geometry_parameters))

    # force_rhr
    print(test_function(force_rhr, force_rhr_parameters))

    # geometry_to_bbox_parameters
    print(test_function(geometry_to_bbox, geometry_to_bbox_parameters))

    if test_dependencies()['osr']:
        # reproject_geometry
        print(test_function(reproject_geometry, reproject_geometry_parameters))

    if test_dependencies()['ogr']:
        # geometry_to_ogr_geometry
        print(test_function(geometry_to_ogr_geometry, geometry_to_ogr_geometry_parameters))

        # ogr_geometry_to_geometry
        print(test_function(ogr_geometry_to_geometry, ogr_geometry_to_geometry_parameters))


if __name__ == '__main__':
    test_all()
