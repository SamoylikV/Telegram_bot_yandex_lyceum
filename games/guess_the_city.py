import os
from random import choice, randint
import requests


def guess_the_city():
    """
    Игра "Угадай город"
    :return: название города
    """
    cities_list = ['Тюмень', 'Москва', 'Екатеринбург']  # Список городов в игре
    orig_path = os.getcwd()
    current_city = choice(cities_list)
    print(current_city)  # Правильный ответ
    try:
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=4" \
                           f"0d1649f-0493-4b70-98ba-98533de771" \
                           f"0b&geocode={current_city}&format=json"
        response = requests.get(geocoder_request)
        json_response = response.json()

        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        pos = toponym['Point']['pos']

        map_request = f'https://static-maps.yandex.ru/' \
                      f'1.x/?ll={pos.split()[0]}%2C{pos.split()[1]}' \
                      f'&spn=0.02,0.02&l=sat'

        response_map = requests.get(map_request)
        map_file = f"guess_maps{current_city}_{randint(0, 100000)}.jpg"

        os.chdir(f'{os.getcwd()}\img')

        with open(map_file, "wb") as file:
            file.write(response_map.content)

        os.chdir(orig_path)

        return [map_file, current_city]
    except Exception:
        os.chdir(orig_path)
        return ['Кажется вы всё сломали']
