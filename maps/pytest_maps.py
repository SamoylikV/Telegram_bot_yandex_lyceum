from pytest import raises as r
from distance import lonlat_distance
from closest_mac import closest_mac
from metro import metro
from pharmacy import pharmacy


def test_lonlat_distance_type_error():
    with r(TypeError):
        lonlat_distance(10, 'lol_kek')


def test_lonlat_distance_value_error():
    with r(ValueError):
        lonlat_distance('lol_kek', 'lol_kek')


def test_closest_mac_wrong_type_1():
    assert closest_mac(123,
                       'lol_kek') == ['Рядом с вами нету макдональдса' \
                                      ' или попробуйте ввести адрес подругому']


def test_closest_mac_wrong_type_2():
    assert closest_mac('lol_kek',
                       123) == ['Рядом с вами нету макдональдса' \
                                ' или попробуйте ввести адрес подругому']


def test_closest_mac_wrong_city():
    assert closest_mac('Кеклолчебурек',
                       'Ленина 10') == ['Рядом с вами нету макдональдса' \
                                        ' или попробуйте в'
                                        'вести адрес подругому']


def test_closest_mac_wrong_address():
    assert closest_mac('Москва',
                       'Кеклолчебурек') == ['Рядом с вами нету макдональдса' \
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


def test_pharmacy_wrong_address():
    assert pharmacy('Москва',
                    'Кеклолчебурек') == ['Рядом с вами нету аптеки']
