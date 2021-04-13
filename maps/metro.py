import requests
import os
from random import randint
from maps.distance import lonlat_distance


def metro(city, address):
    """
    Нахождение ближайшей станции метро
    :param city: Город пользователя
    :param address: Адрес пользователя
    :return: Название станции, названия файла с картой, расстояние до станции
    """
    orig_path = os.getcwd()
    toponym_metro_tochno = 'Рядом с вами нету метро'
    full_adress = f'{city} {address}'
    place = '%20'.join(full_adress.split(' '))
    try:
        geocoder_request_metro = f"http://geocode-m" \
                                 f"aps.yandex.ru/1.x/?apikey=4" \
                                 f"0d1649f-0493" \
                                 f"-4b70-98ba-98533de7710b&" \
                                 f"geocode={place}&format=json"
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
            response_metro = requests.get(geocoder_request_metro)
            json_response_metro = response_metro.json()
            metro_cords = json_response_metro["response"]["GeoObjectC" \
                                                          "ollection"][
                "featureMember"][0]["GeoObject"]["Point"]["pos"]
            metro_coodrinates = metro_cords.split(' ')
            metro_coodrinates = ','.join(metro_coodrinates)
            metro_coodrinates = ''.join(metro_coodrinates)

            toponym_metro = \
                json_response_metro["response"]["GeoObjectCollection"][
                    "featureMember"][0]["GeoObject"]

            toponym_metro_tochno = \
                toponym_metro["metaDataProperty"]['GeocoderMetaData'][
                    'AddressDetails']['Country']['AdministrativeArea'][
                    'Locality'][
                    'Thoroughfare']['Premise']['PremiseName'][6::]

            os.chdir(f'{os.getcwd()}\img')

            map_request = f"https://static-maps.yandex.ru/1" \
                          f".x/?ll={metro_coodrinates}&spn=0" \
                          f".01,0.01&l=map&pt={metro_coodrinates},comma"

            response_map = requests.get(map_request)
            map_file = f"metro_map{randint(0, 100000)}.png"
            with open(map_file, "wb") as file:
                file.write(response_map.content)

            os.chdir(orig_path)
            return [toponym_metro_tochno, map_file,
                    lonlat_distance((toponym_coodrinates_metro.split(',')[0],
                                     toponym_coodrinates_metro.split(',')[1]),
                                    (metro_cords.split(' ')[0],
                                     metro_cords.split(' ')[1]))]
        else:

            os.chdir(orig_path)
            return [toponym_metro_tochno]
    except Exception as e:
        print(e)
        os.chdir(orig_path)
        return [toponym_metro_tochno]
