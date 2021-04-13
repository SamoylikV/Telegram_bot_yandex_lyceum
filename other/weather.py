import requests


def weather(city):
    slovar = {}
    try:
        s_city = f"{city},RU"
        appid = "16093ac52a4bd20f7c5f8db6d77a53eb"
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'q': s_city, 'units': 'metric',
                                   'lang': 'ru', 'APPID': appid})
        data = res.json()
        slovar['temp'] = data['main']['temp']
        slovar['conditions'] = data['weather'][0]['description']
    except Exception:
        slovar['temp'] = None
        slovar['conditions'] = None
    return slovar
