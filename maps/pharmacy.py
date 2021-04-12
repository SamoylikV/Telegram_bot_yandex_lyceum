import requests
import os
from random import randint
from maps.distance import lonlat_distance


def pharmacy(city, address):
    orig_path = os.getcwd()
    toponym_pharmacy_tochno = 'Рядом с вами нету аптеки'
    full_adress = f'{city} {address}'
    place = '%20'.join(full_adress.split(' '))

    try:
        geocoder_request_pharmacy = f"http://geocode-m" \
                                    f"aps.yandex.ru/1.x/?apikey=4" \
                                    f"0d1649f-0493" \
                                    f"-4b70-98ba-98533de7710b&" \
                                    f"geocode={place}&format=json"
        response_pharmacy = requests.get(geocoder_request_pharmacy)
        json_response_pharmacy = response_pharmacy.json()

        toponym = json_response_pharmacy["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude = toponym_coodrinates.split(" ")[0]
        toponym_lattitude = toponym_coodrinates.split(" ")[1]

        address_ll = ','.join([toponym_longitude, toponym_lattitude])

        search_params = {
            "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
            "text": "аптека",
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz",
            'results': 1
        }

        response = requests.get('https://search-maps.yandex.ru/v1/',
                                params=search_params)
        json_response = response.json()
        pharmacy_coords = json_response['features'][0]['geometry'][
            'coordinates']

        os.chdir(f'{os.getcwd()}\img')

        pharmacy_coords[0] = str(pharmacy_coords[0])
        pharmacy_coords[1] = str(pharmacy_coords[1])

        map_request = f"https://static-maps.yandex.ru/1" \
                      f".x/?ll={','.join(pharmacy_coords)}&spn=0" \
                      f".01,0.01&l=map&pt={','.join(pharmacy_coords)},comma"
        response_map = requests.get(map_request)
        pharmacy_map_file = f"pharmacy_map{randint(0, 100000)}.png"

        with open(pharmacy_map_file, "wb") as file:
            file.write(response_map.content)

        os.chdir(orig_path)

        return [pharmacy_map_file,
                lonlat_distance((toponym_longitude, toponym_lattitude), (
                    pharmacy_coords[0], pharmacy_coords[1]))]

    except Exception as e:
        print(e)
        os.chdir(orig_path)
        return [toponym_pharmacy_tochno]
