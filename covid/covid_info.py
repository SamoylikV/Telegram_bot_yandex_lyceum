import requests
import datetime
import time

dumb_touple = {'Московская область': '1', 'Санкт-Петербург': '2', 'Москва': '213', 'Россия': '225',
               'Севастополь': '959', 'Республика Крым': '977', 'Ленинградская область': '10174',
               'Ненецкий автономный округ': '10176', 'Республика Алтай': '10231', 'Республика Тыва': '10233',
               'Еврейская автономная область': '10243', 'Чукотский автономный округ': '10251',
               'Белгородская область': '10645', 'Брянская область': '10650', 'Владимирская область': '10658',
               'Воронежская область': '10672', 'Ивановская область': '10687', 'Калужская область': '10693',
               'Костромская область': '10699', 'Курская область': '10705', 'Липецкая область': '10712',
               'Орловская область': '10772', 'Рязанская область': '10776', 'Смоленская область': '10795',
               'Тамбовская область': '10802', 'Тверская область': '10819', 'Тульская область': '10832',
               'Ярославская область': '10841', 'Архангельская область': '10842', 'Вологодская область': '10853',
               'Калининградская область': '10857', 'Мурманская область': '10897', 'Новгородская область': '10904',
               'Псковская область': '10926', 'Республика Карелия': '10933', 'Республика Коми': '10939',
               'Астраханская область': '10946', 'Волгоградская область': '10950', 'Краснодарский край': '10995',
               'Республика Адыгея': '11004', 'Республика Дагестан': '11010', 'Республика Ингушетия': '11012',
               'Кабардино-Балкарская Республика': '11013', 'Республика Калмыкия': '11015',
               'Карачаево-Черкесская Республика': '11020', 'Республика Северная Осетия — Алания': '11021',
               'Чеченская Республика': '11024', 'Ростовская область': '11029', 'Ставропольский край': '11069',
               'Кировская область': '11070', 'Республика Марий Эл': '11077', 'Нижегородская область': '11079',
               'Оренбургская область': '11084', 'Пензенская область': '11095', 'Пермский край': '11108',
               'Республика Башкортостан': '11111', 'Республика Мордовия': '11117', 'Республика Татарстан': '11119',
               'Самарская область': '11131', 'Саратовская область': '11146', 'Удмуртская Республика': '11148',
               'Ульяновская область': '11153', 'Чувашская Республика': '11156', 'Курганская область': '11158',
               'Свердловская область': '11162', 'Тюменская область': '11176',
               'Ханты-Мансийский автономный округ — Югра': '11193', 'Челябинская область': '11225',
               'Ямало-Ненецкий автономный округ': '11232', 'Алтайский край': '11235', 'Иркутская область': '11266',
               'Кемеровская область': '11282', 'Красноярский край': '11309', 'Новосибирская область': '11316',
               'Омская область': '11318', 'Республика Бурятия': '11330', 'Республика Хакасия': '11340',
               'Томская область': '11353', 'Амурская область': '11375', 'Камчатский край': '11398',
               'Магаданская область': '11403', 'Приморский край': '11409', 'Республика Саха (Якутия)': '11443',
               'Сахалинская область': '11450', 'Хабаровский край': '11457', 'Забайкальский край': '21949'}


def global_stats():
    glob_stats = []
    response = requests.get("https://disease.sh/v3/covid-19/all")
    data = response.json()
    glob_stats.append(data['cases']),
    glob_stats.append(data['todayCases']),
    glob_stats.append(data['deaths']),
    glob_stats.append(data['todayDeaths']),
    glob_stats.append(data['recovered']),
    glob_stats.append(data['todayRecovered']),
    glob_stats.append(data['active'])
    return glob_stats


def all_countries(country_):
    countries = []
    stats = []
    response = requests.get("https://disease.sh/v3/covid-19/countries?sort=cases")
    data = response.json()
    try:
        for country in data:
            if "'" in country["country"]:
                country["country"] = country["country"].replace("'", "''")
            if country["country"].lower() == country_.lower():
                stats.append(country["cases"]),
                stats.append(country["todayCases"]),
                stats.append(country["deaths"]),
                stats.append(country["todayDeaths"]),
                stats.append(country["recovered"]),
                stats.append(country["todayRecovered"]),
                stats.append(country["critical"]),
                stats.append(country["active"]),
                stats.append(country["casesPerOneMillion"]),
                stats.append(country["deathsPerOneMillion"]),
                stats.append(country["tests"])

            countries.append(country['country'])
    except Exception:
        print(123)
        try:
            response = requests.get('http://milab.s3.yandex.net/2020/covid19-stat/data/v10/default_data.json').json()[
                'russia_stat_struct']['data']
            stats = []
            if country_ in dumb_touple:
                stats.append(response[dumb_touple[country_]]['info']['cases'])
                stats.append(response[dumb_touple[country_]]['info']['cases_delta'])
                stats.append(response[dumb_touple[country_]]['info']['deaths'])
                stats.append(response[dumb_touple[country_]]['info']['deaths_delta'])
        except Exception:
            pass
    return stats


global_stats()
