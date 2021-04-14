import requests
import os
from maps.distance import lonlat_distance
from random import randint


def closest_mac(city, address):
    """
    Нахождение ближайшего макдональдса
    :param city: Город пользователя
    :param address: Адрес пользователя
    :return: Название файла с картой, название макдональдса,
    расстояние до макдональда, адрес, время работы
    """
    orig_path = os.getcwd()
    toponym_pharmacy_tochno = 'Рядом с вами нету макдон' \
                              'альдса или попробуйте ввести адрес подругому'
    try:
        full_adress = f'{city} {address}'
        place = '%20'.join(' '.join(full_adress.split('-')).split(', '))

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": place,
            "format": "json"}

        response_map = requests.get(geocoder_api_server,
                                    params=geocoder_params)

        if not response_map:
            pass

        json_response_map = response_map.json()
        address_ll = json_response_map["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]['Point']['pos']
        address_ll = ','.join(address_ll.split())

        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
        search_params = {
            "apikey": api_key,
            "text": "Макдональдс",
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz"
        }

        response_map = requests.get(search_api_server, params=search_params)
        json_response_map = response_map.json()

        org = json_response_map["features"][0]
        point = org["geometry"]["coordinates"]
        first_point = f"{point[0]},{point[1]}"

        map_params = {
            "l": "map",
            'pt': f'{address_ll},pm2al~{first_point},pm2bl'}

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response_map = requests.get(map_api_server, params=map_params)

        start_point = list(map(float, address_ll.split(',')))
        org_point = org['geometry']['coordinates']

        os.chdir(f'{os.getcwd()}\img')

        pharmacy_map_file = f"closest_mac_map{randint(0, 100000)}.png"
        with open(pharmacy_map_file, "wb") as file:
            file.write(response_map.content)

        name = org['properties']['name']
        address_ = org['properties']['description']
        time_of_work = org['properties']['CompanyMetaData']['Hours'][
            'text']

        distance = int(lonlat_distance(start_point, org_point))
        os.chdir(orig_path)
        return [pharmacy_map_file, name, distance, address_, time_of_work]
    except Exception:
        return [toponym_pharmacy_tochno]
