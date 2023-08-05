from geoformat.geoprocessing.measure.area import (
    shoelace_formula
)

from test_all import test_function

shoelace_formula_parameters = {
    0: {
        "ring_coordinates": [[-1, 1], [1, 1], [1, -1], [-1, -1]],  # convex boundary
        "absolute_value": True,
        "return_value": 4.
    },
    1: {
        "ring_coordinates": [[-1, -1], [1, -1], [1, 1], [-1, 1]],  # reverse convex boundary
        "absolute_value": True,
        "return_value": 4.
    },
    2: {
        "ring_coordinates": [[-1, -1], [0, 0], [1, -1], [1, 1], [-1, 1]],  # concave boundary
        "absolute_value": True,
        "return_value": 3.
    },
    3: {
        "ring_coordinates": [[-1, 1], [1, 1], [1, -1], [0, 0], [-1, -1]],  # reverse concave boundary
        "absolute_value": True,
        "return_value": 3.
    },
    4: {
        "ring_coordinates": [[-1, 1], [1, 1], [1, -1], [-1, -1]],  # convex boundary
        "absolute_value": False,
        "return_value": 4.
    },
    5: {
        "ring_coordinates": [[-1, -1], [1, -1], [1, 1], [-1, 1]],  # reverse convex boundary
        "absolute_value": False,
        "return_value": -4.
    },
    6: {
        "ring_coordinates": [[-1, -1], [0, 0], [1, -1], [1, 1], [-1, 1]],  # concave boundary
        "absolute_value": False,
        "return_value": -3.
    },
    7: {
        "ring_coordinates": [[-1, 1], [1, 1], [1, -1], [0, 0], [-1, -1]],  # reverse concave boundary
        "absolute_value": False,
        "return_value": 3.
    },
}


def test_all():
    # shoelace_formula
    print(test_function(shoelace_formula, shoelace_formula_parameters))


if __name__ == '__main__':
    test_all()
