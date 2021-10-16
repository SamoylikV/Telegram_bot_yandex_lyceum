from telegram.ext import *
from telegram import *
from other.weather import weather
from other.comments import comments
from maps.metro import metro
from maps.pharmacy import pharmacy
from maps.closest_mac import closest_mac
from games.guess_the_city import guess_the_city
from games.dice import throw_a_cube, dice
from covid.covid_info import global_stats, all_countries
from covid.infographics import death_graph, vaccine_graph, new_cases_graph
import argparse
import requests

parser = argparse.ArgumentParser()

try:
    parser.add_argument("token", nargs="*")
    args = parser.parse_args()
    updater_ = Updater(args.token[0])
except Exception:
    try:
        f = open("token.txt", encoding="utf8")
        updater_ = Updater(f.readlines()[-1])
    except Exception:
        print('Введите правильный токен')

try:
    p = open("pass.txt", encoding="utf8")
    admin_pass = p.readlines()[0]
except Exception:
    admin_pass = 'Vasiliy_Samoylik_the_best_person_on_the_Earth'

user_name = ''  # Переменная с именем пользователя
user_city = ''  # Переменная с городом пользователя
user_address = ''  # Переменная с адресом пользователя
user_comment = ''  # Переменная с комментарием пользователя
country = ''
current_city = ''  # Переменная с текущим городом в игре "Угадай город"
try_counter = 0  # Счёичмк попыток в игре "Угадай город"
game_is_played = False  # Переменная с состаянием игры "Угадай город"
is_admin = True  # Переменна яс состоянием меню админа
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
keyboard_main = [['🦠 Covid-19'],
                 ['🌤 Узнать погоду', '🖊️ Написать отзыв', '🌆 Ввести новый адрес'],
                 ['🚇 Найти ближайшее метро', '🍟 Найти ближайший макдональдс',
                  '🏥 Показать аптеки недалеко от вас'],
                 ['🎮 Игры']]
keyboard_games = [['🌆 Угадай город', '🎲 Кинуть кубик'],
                  ['🕶 Основные функции']]
covid_keyboard = [['🦠 В регионах', '🦠 В странах'],
                  ['🕶 Основные функции']]
keyboard_admin = [['Перезапустить бота']]
keyboard = keyboard_main


def main():
    global updater_
    dp = updater_.dispatcher
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        states={
            1: [MessageHandler(Filters.text, get_city)],
            2: [MessageHandler(Filters.text, get_address)],
            3: [MessageHandler(Filters.text, second_start)],
            4: [MessageHandler(Filters.text, get_comments)],
            5: [MessageHandler(Filters.text, text_commands)],
            6: [MessageHandler(Filters.text, get_covid_info_reg)],
            7: [MessageHandler(Filters.text, get_covid_info_coun)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)


def start(update, context):
    """
    Приветствуем пользователя и просим ввести его данные о геолокации
    """
    global user_city
    global is_admin
    update.message.reply_text(
        'Введите ваш город и адрес, '
        'чтобы разблокировать весь функционал бота')
    update.message.reply_text('Введите город',
                              reply_markup=ReplyKeyboardRemove())
    return 1


def get_city(update, context):
    """
    Получаем город пользователя
    """
    global user_city
    user_city = update.message.text
    update.message.reply_text('Введите адрес')
    return 2


def get_address(update, context):
    """
    Получаем адрес пользователя
    """
    global user_address
    user_address = update.message.text
    reply_keyboard = [['Да', 'Нет']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(f'Ваш город: {user_city}')
    update.message.reply_text(f'Ваш адрес: {user_address}')
    update.message.reply_text('Вы правильно ввели данные?',
                              reply_markup=markup)
    return 3


def second_start(update, context):
    """
    Уточняем правильно ли пользователь ввёл данные
    и выводим клавиатуру с главным меню
    """
    global user_city
    if update.message.text == 'Нет':
        update.message.reply_text('Введите город')
        return 1
    else:
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text('Выберите действие',
                                  reply_markup=markup)
    return 5


def get_weather(update, context):
    """
    Выводим значение температуры пользователю
    """
    global user_city
    if weather(user_city)["conditions"] is not None:
        update.message.reply_text(
            f'В городе {user_city} {weather(user_city)["conditions"]}')
        update.message.reply_text(
            f'Температура: {weather(user_city)["temp"]}C')
    else:
        update.message.reply_text(
            'Проверьте написание города и повторите попытку')


def get_metro(update, context):
    """
    Проверяем наличие метро возле пользователя и выводим карту
    """
    global user_city
    global user_address
    metro_is_near = True
    metro_name = metro(user_city, user_address)[0]
    try:
        file_name = metro(user_city, user_address)[1]
        to_metro_distance = metro(user_city, user_address)[2]
    except Exception as e:
        metro_is_near = False
    if metro_name != 'Рядом с вами нету метро' and metro_is_near is True:
        update.message.reply_photo(photo=open(f'img/{file_name}', 'rb'))
        update.message.reply_text(
            f'Ближайшая к вам станция метро: {metro_name}')
        update.message.reply_text(
            f'Расстояние до станции: {to_metro_distance}м')
    else:
        update.message.reply_text(
            f'Сейчас бы метро в {user_city} искать')


def get_pharmacy(update, context):
    """
    Выводим ближайшие 10 аптек в городе
    """
    global user_city
    global user_address
    try:
        file_name = pharmacy(user_city, user_address)[0]
        update.message.reply_photo(photo=open(f'img/{file_name}', 'rb'))
    except Exception:
        update.message.reply_text(
            f'Рядом с вами нету аптеки, земля вам пухом!')


def get_closest_mac(update, context):
    """
    Выводим ближайший макдональдс к пользователю
    """
    global user_city
    global user_address
    try:
        file_name = closest_mac(user_city, user_address)[0]
        pharmacy_name = closest_mac(user_city, user_address)[1]
        distance_to_pharmacy = closest_mac(user_city, user_address)[2]
        pharmacy_address = closest_mac(user_city, user_address)[3]
        pharmacy_time_of_works = closest_mac(user_city, user_address)[4]
        update.message.reply_photo(photo=open(f'img/{file_name}', 'rb'))
        update.message.reply_text(
            f'{pharmacy_name} {pharmacy_time_of_works}')
        update.message.reply_text(
            f'Расстояние до {pharmacy_address}: {distance_to_pharmacy}м')
    except Exception as e:
        print(e)
        update.message.reply_text(
            f'Рядом с вами нету Макдональдса, удачи не помереть с голоду!')


def get_comments(update, context):
    """
    Получаем отзыв от пользователя 
    """
    global user_comment
    global user_name
    user_name = update.message.from_user.username
    user_comment = update.message.text
    return 5


def text_commands(update, context):
    """
    Функция обработки текстовых команд с клавиатуры
    """
    global user_comment
    global keyboard
    global current_city
    global game_is_played
    global is_admin
    global try_counter

    # Возвращение в начало
    if update.message.text == '/start':
        update.message.reply_text(
            'Введите ваш город и адрес, что'
            'бы разблокировать весь функционал бота')
        update.message.reply_text('Введите город')
        return 1

    # Ввод нового адреса
    if update.message.text == '🌆 Ввести новый адрес':
        update.message.reply_text('Введите город')
        return 1

    # Ввод отзыва
    if update.message.text == '🖊️ Написать отзыв':
        reply_keyboard = [['Подтвердить']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            f'Сюда вы можете написать ваш отзыв', reply_markup=markup)
        return 4

    # Подтверждение отзыва
    if update.message.text == 'Подтвердить':
        print("user_comment =", user_comment)
        markup = ReplyKeyboardMarkup(keyboard)
        if user_comment != '':
            update.message.reply_text('Ваш отзыв успешно записан!',
                                      reply_markup=markup)
            comments(user_comment, user_name)
            user_comment = ''
        else:
            update.message.reply_text('Ваш отзыв пуст',
                                      reply_markup=markup)

    if update.message.text == '/graph_vaccine':
        update.message.reply_photo(update.message.reply_photo(photo=open(f'img/{vaccine_graph(country)}', 'rb')))
        return 5

    if update.message.text == '/graph_death':
        update.message.reply_photo(update.message.reply_photo(photo=open(f'img/{death_graph(country)}', 'rb')))
        return 5

    if update.message.text == '/graph_new_cases':
        update.message.reply_photo(update.message.reply_photo(photo=open(f'img/{new_cases_graph(country)}', 'rb')))
        return 5

    # Обрабтока команды вывода погоды
    if update.message.text == '🌤 Узнать погоду':
        get_weather(update, context)

    # Обрабтока команды вывода метро
    if update.message.text == '🚇 Найти ближайшее метро':
        get_metro(update, context)

    # Обрабтока команды вывода аптек города
    if update.message.text == '🏥 Показать аптеки недалеко от вас':
        get_pharmacy(update, context)

    # Обрабтока команды вывода ближайшего макдональдса
    if update.message.text == '🍟 Найти ближайший макдональдс':
        get_closest_mac(update, context)

    # Обрабтока команды на смены клавиатуры на игровую
    if update.message.text == '🎮 Игры':
        keyboard = keyboard_games
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(
            f'Переключаю на клавиатуру "{update.message.text}"',
            reply_markup=markup)

    # Обрабтока команды на смены клавиатуры на основную
    if update.message.text == '🕶 Основные функции':
        keyboard = keyboard_main
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(
            f'Переключаю на клавиатуру "{update.message.text}"',
            reply_markup=markup)

    # Обрабтока команды на начало игры "Угадай город"
    if update.message.text == '🌆 Угадай город':
        reply_keyboard = [['Сдаться']]
        markup = ReplyKeyboardMarkup(reply_keyboard)
        map_file, current_city = guess_the_city()
        update.message.reply_text(
            f'Напишите названия этого города', reply_markup=markup)
        update.message.reply_photo(
            photo=open(f'img/{map_file}', 'rb'))
        game_is_played = True
        print(current_city)

    # Обрабтока команды на сдачу в игре "Угадай город"
    if update.message.text == 'Сдаться' or try_counter >= 10:
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(f'Это был город: {current_city}',
                                  reply_markup=markup)
        try_counter = 0
        game_is_played = False
        current_city = ''

    if update.message.text == '🦠 Covid-19':
        markup = ReplyKeyboardMarkup(covid_keyboard)
        update.message.reply_text('Теперь у вас включена клавиатура "Covid"', reply_markup=markup)

    if update.message.text == '🦠 В регионах':
        update.message.reply_text('Введите ваш регион')
        return 6

    if update.message.text == '🦠 В странах':
        update.message.reply_text('Введите вашу страну (на английском языке)')
        update.message.reply_text('Что-бы вывести общию статистику нажмите /tut')
        return 7

    # Проверка правильности ответа в игре "Угадай город"
    if game_is_played is True:
        try_counter += 1
        if update.message.text == current_city:
            markup = ReplyKeyboardMarkup(keyboard)
            update.message.reply_text(
                f'Правильно! Это был город: {current_city}',
                reply_markup=markup)
            try_counter = 0
            game_is_played = False
        elif game_is_played is True \
                and update.message.text != current_city and try_counter >= 2:
            update.message.reply_text(
                f'Неверно или ничего не написано, '
                f'осталось {11 - try_counter} попыток')

    # Возвращение в меню игр
    if update.message.text == '⏪ Вернуться назад':
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text('Возвращаемся назад', reply_markup=markup)

    # Кидаемй кубик
    if update.message.text == '🎲 Кинуть кубик':
        dice(update, context)

    # Кидаем один шестигранный кубик
    if update.message.text == '🎲 Кинуть один шестигранный кубик':
        update.message.reply_text(' '.join(throw_a_cube(6)))

    # Кидаем 2 шестигранных кубика одновременно
    if update.message.text == '🎲 🎲Кинуть 2 шестигранных кубика одновременно':
        update.message.reply_text(' '.join(throw_a_cube(6, 2)))

    # Кидаем 20-гранный кубик
    if update.message.text == '🎱 Кинуть 20-гранный кубик':
        update.message.reply_text(' '.join(throw_a_cube(20)))

    # Вход в админ панель
    if update.message.text == admin_pass:
        is_admin = True
        markup = ReplyKeyboardMarkup(keyboard_admin)
        update.message.reply_text(
            'Вы получили доступ к админ панели', reply_markup=markup)

    # Обработка команды с админ клавиатуры на перезапуск бота
    if update.message.text == 'Перезапустить бота':
        markup = ReplyKeyboardMarkup(keyboard)
        if is_admin is True:
            update.message.reply_text('Перезапускаю...')
            update.message.reply_text(
                'Введите ваш город и адрес, что'
                'бы разблокировать весь функционал бота',
                reply_markup=ReplyKeyboardRemove())
            update.message.reply_text('Введите город')
            return 1
        else:
            update.message.reply_text('Кажется вы не админ',
                                      reply_markup=markup)


def get_covid_info_coun(update, context):
    global country
    country = update.message.text
    if country != '/tut':
        update.message.reply_text(f'Статистика по стране {country}')
        try:
            update.message.reply_text(f'🦠 Всего случаев: {"{:,}".format(all_countries(country)[0])}\n'
                                      f'🦠 Случаев за последние 24 часа: {"{:,}".format(all_countries(country)[1])}\n'
                                      f'💀 Смертей: {"{:,}".format(all_countries(country)[2])}\n'
                                      f'💀 Смертей за последние 24 часа: {"{:,}".format(all_countries(country)[3])}\n'
                                      f'🍀 Вылечено: {"{:,}".format(all_countries(country)[4])}\n'
                                      f'🍀 Вылечено за последние 24 часа: {"{:,}".format(all_countries(country)[5])}\n'
                                      f'🚨 В критическом состоянии: {"{:,}".format(all_countries(country)[6])}\n'
                                      '/graph_vaccine - Нажми что бы увидеть график вакцинирования\n'
                                      '/graph_death - Нажми что бы увидеть график смертности\n'
                                      '/graph_new_cases - Нажми что бы увидеть график заражений\n'
                                      )
        except Exception as s:
            print(s)
            update.message.reply_text('Возможно вы ввели страну с ошибкой или на русском языке')
            return 5
    else:
        update.message.reply_text(f'🦠 Всего случаев: {"{:,}".format(global_stats()[0])}\n'
                                  f'🦠 Случаев за последние 24 часа: {"{:,}".format(global_stats()[1])}\n'
                                  f'💀 Смертей: {"{:,}".format(global_stats()[2])}\n'
                                  f'💀 Смертей за последние 24 часа: {"{:,}".format(global_stats()[3])}\n'
                                  f'🍀 Вылечено: {"{:,}".format(global_stats()[4])}\n'
                                  f'🍀 Вылечено за последние 24 часа: {"{:,}".format(global_stats()[5])}')
        country = ''
    return 5


def get_covid_info_reg(update, context):
    global country
    country = update.message.text
    print(country)
    response = \
        requests.get('http://milab.s3.yandex.net/2020/covid19-stat/data/v10/default_data.json').json()[
            'russia_stat_struct']['data']
    stats = []
    if country in dumb_touple:
        stats.append(response[dumb_touple[country]]['info']['cases'])
        stats.append(response[dumb_touple[country]]['info']['cases_delta'])
        stats.append(response[dumb_touple[country]]['info']['deaths'])
        stats.append(response[dumb_touple[country]]['info']['deaths_delta'])

        update.message.reply_text(f'🦠 Всего случаев: {"{:,}".format(stats[0])}\n'
                                  f'🦠 Случаев за последние 24 часа: {"{:,}".format(stats[1])}\n'
                                  f'💀 Смертей: {"{:,}".format(stats[2])}\n'
                                  f'💀 Смертей за последние 24 часа: {"{:,}".format(stats[3])}\n'
                                  )
    return 5


def stop(update, context):
    update.message.reply_text(
        "До свидания")
    return ConversationHandler.END  # Константа, означающая конец диалога.


if __name__ == '__main__':
    main()
    try:
        updater_.start_polling()
        updater_.idle()
    except Exception:
        pass
