from pytest import raises as r
from dice import throw_a_cube


def test_lonlat_distance_type_error():
    with r(TypeError):
        throw_a_cube('10')


def test_lonlat_distance_type_error_2():
    with r(TypeError):
        throw_a_cube(10, '1')


def test_lonlat_distance_type_error_3():
    with r(TypeError):
        throw_a_cube('10', '1')
