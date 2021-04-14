from pytest import raises as r
from maps.distance import lonlat_distance
from maps.closest_mac import closest_mac
from maps.metro import metro
from maps.pharmacy import pharmacy
from other.weather import weather
from games.dice import throw_a_cube


def test_lonlat_distance_type_error():
    with r(TypeError):
        lonlat_distance(10, 'lol_kek')


def test_lonlat_distance_value_error():
    with r(ValueError):
        lonlat_distance('lol_kek', 'lol_kek')


def test_closest_mac_wrong_type_1():
    assert closest_mac(123,
                       '?"№;РНЫА@&#4') == ['Рядом с вами нету макдональдса' \
                                           ' или попробуйте ввести адрес подругому']


def test_closest_mac_wrong_type_2():
    assert closest_mac('?"№;РНЫА@&#4',
                       123) == ['Рядом с вами нету макдональдса' \
                                ' или попробуйте ввести адрес подругому']


def test_closest_mac_wrong_city():
    assert closest_mac('?"№;РНЫА@&#4',
                       'Ленина 10') == ['Рядом с вами нету макдональдса' \
                                        ' или попробуйте в'
                                        'вести адрес подругому']


def test_metro_wrong_type_1():
    assert metro(123,
                 'Кеклолчебурек') == ['Рядом с вами нету метро']


def test_metro_wrong_type_2():
    assert metro('Кеклолчебурек',
                 123) == ['Рядом с вами нету метро']


def test_metro_wrong_city():
    assert metro('Кеклолчебурек',
                 'Ленина 10') == ['Рядом с вами нету метро']


def test_metro_wrong_address():
    assert metro('Москва',
                 'Кеклолчебурек') == ['Рядом с вами нету метро']


def test_pharmacy_wrong_type_1():
    assert pharmacy(123,
                    'Кеклолчебурек') == ['Рядом с вами нету аптеки']


def test_pharmacy_wrong_type_2():
    assert pharmacy('Кеклолчебурек',
                    123) == ['Рядом с вами нету аптеки']


def test_pharmacy_wrong_city():
    assert pharmacy('Кеклолчебурек',
                    'Ленина 10') == ['Рядом с вами нету аптеки']


def test_weather_wrong_type():
    assert weather(123) == {'temp': None, 'conditions': None}


def test_weather_wrong_city():
    assert weather('lol_kek') == {'temp': None, 'conditions': None}


def test_throw_a_cube_type_error():
    with r(TypeError):
        throw_a_cube('10')


def test_throw_a_cube_type_error_2():
    with r(TypeError):
        throw_a_cube(10, '1')


def test_throw_a_cube_type_error_3():
    with r(TypeError):
        throw_a_cube('10', '1')
