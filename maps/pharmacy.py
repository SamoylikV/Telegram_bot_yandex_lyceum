import requests
import os
from random import randint


def pharmacy(city, address):
    """
    Нахождение аптек в городе
    :return: Название файла с картой
    """
    orig_path = os.getcwd()
    toponym_pharmacy_tochno = 'Рядом с вами нету аптеки'
    new_points = []
    try:
        full_adress = f'{address} {city}'
        place = '%20'.join(' '.join(full_adress.split('-')).split(' '))
        points = []
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
        print(place)
        response = requests.get(f"http://geocode-m" \
                                f"aps.yandex.ru/1.x/?apikey=4" \
                                f"0d1649f-0493" \
                                f"-4b70-98ba-98533de7710b&" \
                                f"geocode={'%20'.join(city.split(' '))}%20{'%20'.join(address.split(' '))}&format=json")

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude = toponym_coodrinates.split(" ")[0]
        toponym_lattitude = toponym_coodrinates.split(" ")[1]

        address_ll = ','.join([toponym_longitude, toponym_lattitude])
        search_params = {
            "apikey": api_key,
            "text": "аптека",
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz",
            'results': 10
        }

        response = requests.get(search_api_server, params=search_params)
        json_response = response.json()
        for i in range(10):
            coords = json_response['features'][i]['geometry'][
                'coordinates']
            points.append((coords))

        for coords in points:
            new_points.append(','.join([*list(map(str, coords)), 'pm2dgl']))

        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "l": "map",
            'pt': '~'.join(new_points)
        }

        os.chdir(f'{os.getcwd()}\img')
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response_map = requests.get(map_api_server, params=map_params)

        pharmacy_map_file = f"pharmacy_map{randint(0, 100000)}.png"

        with open(pharmacy_map_file, "wb") as file:
            file.write(response_map.content)

        os.chdir(orig_path)

        return [pharmacy_map_file]
    except Exception as e:
        print(e)
        return [toponym_pharmacy_tochno]
