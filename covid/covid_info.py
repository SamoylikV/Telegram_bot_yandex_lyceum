import requests
import datetime
import time


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
    for country in data:
        try:
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
            return 'Возможно вы ввели страну с ошибкой или на русском языке, пожалуйста введите правильно и на английском'
    return stats


global_stats()
