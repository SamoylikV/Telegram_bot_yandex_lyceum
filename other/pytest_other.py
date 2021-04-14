from pytest import raises as r
from weather import weather


def test_closest_mac_wrong_type():
    assert weather(123) == {'temp': None, 'conditions': None}


def test_closest_mac_wrong_city():
    assert weather('lol_kek') == {'temp': None, 'conditions': None}
