import requests


def weather(city):
    s_city = f"{city},RU"
    slovar = {}
    appid = "16093ac52a4bd20f7c5f8db6d77a53eb"
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'q': s_city, 'units': 'metric',
                               'lang': 'ru', 'APPID': appid})
    data = res.json()

    slovar['temp'] = data['main']['temp']
    slovar['conditions'] = data['weather'][0]['description']
    return slovar
