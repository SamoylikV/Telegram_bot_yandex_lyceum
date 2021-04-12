import requests
import os
from random import randint
import shutil


def metro(city, address):
    orig_path = os.getcwd()
    toponym_metro_tochno = 'Рядом с вами нету метро'
    full_adress = f'{city} {address}'
    place = '%20'.join(full_adress.split(' '))
    try:
        geocoder_request_metro = f"http://geocode-maps.yandex.ru/1.x/?apikey=4" \
                                 f"0d1649f-0493" \
                                 f"-4b70-98ba-98533de7710b&geocode={place}&format=json"
        geocoder_request_city = f"http://geocode-maps.yandex.ru/1.x/?apikey=4" \
                                f"0d1649f-0493" \
                                f"-4b70-98ba-98533de7710b&geocode={city}&format=json"
        response_metro = requests.get(geocoder_request_metro)
        if response_metro:
            json_response_metro = response_metro.json()
            toponym = \
                json_response_metro["response"]["GeoObjectCollection"][
                    "featureMember"][
                    0][
                    "GeoObject"]
            # Координаты центра топонима:
            toponym_coodrinates_metro = toponym["Point"]["pos"]
            toponym_coodrinates_metro = toponym_coodrinates_metro.split(' ')
            toponym_coodrinates_metro = ','.join(toponym_coodrinates_metro)
            toponym_coodrinates_metro = ''.join(toponym_coodrinates_metro)
            geocoder_request_metro = f'https://geocode-maps.yandex.ru/1.x' \
                                     f'/?apikey=40d1649f-0493-4b70-98ba' \
                                     f'-98533de7710b&geocode=' \
                                     f'{toponym_coodrinates_metro}&kind=met' \
                                     f'ro&results' \
                                     f'=1&format=json'
            print()
            response_metro = requests.get(geocoder_request_metro)
            json_response_metro = response_metro.json()

            toponym_metro = \
                json_response_metro["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]

            toponym_metro_tochno = \
                toponym_metro["metaDataProperty"]['GeocoderMetaData'][
                    'AddressDetails']['Country']['AdministrativeArea'][
                    'Locality'][
                    'Thoroughfare']['Premise']['PremiseName'][6::]

            toponym_coodrinates_city = toponym["Point"]["pos"]
            toponym_coodrinates_city = toponym_coodrinates_city.split(' ')
            toponym_coodrinates_city = ','.join(toponym_coodrinates_city)
            toponym_coodrinates_city = ''.join(toponym_coodrinates_city)
            os.chdir(f'{os.getcwd()}\img')

            map_request = f"https://static-maps.yandex.ru/1" \
                          f".x/?ll={toponym_coodrinates_city}&spn=0" \
                          f".1,0.1&l=map&pt={toponym_coodrinates_metro},comma"
            response_map = requests.get(map_request)
            map_file = f"metro_map{randint(0, 10000)}.png"

            with open(map_file, "wb") as file:
                file.write(response_map.content)
            os.chdir(orig_path)
            return [toponym_metro_tochno, map_file]
        else:
            os.chdir(orig_path)
            return [toponym_metro_tochno]
    except Exception:
        os.chdir(orig_path)
        return [toponym_metro_tochno]
