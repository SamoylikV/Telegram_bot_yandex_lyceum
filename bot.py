from telegram.ext import *
from telegram import *
from other.weather import weather
from other.comments import comments
from maps.metro import metro
from maps.pharmacy import pharmacy
from games.guess_the_city import guess_the_city
import random

# TODO: расписать файлы с нужными функциями
# TODO: получаем город пользователя, и выдаём ему погоду ----------------------
# TODO: показываем карту города, и просим его угадать--------------------------
# TODO: найти ближайшую станцию метро, дистанция до неё -----------------------
# TODO: найти ближайшую аптеку тоже из задачи ---------------------------------
# TODO: попробовать что нибудь с новостями придумать https://pypi.org/project/GoogleNews/
# TODO: сделать всё красиво по файлам
# TODO: Сделать клавиаутуру у пользователя что бы всё тоже было красиво--------
# TODO: ну и коменты расписать

f = open("token.txt", encoding="utf8")
updater = Updater(f.readlines()[0])

user_name = ''
user_city = ''
user_address = ''
user_comment = ''
user_answer = ''
current_city = ''
game_is_played = False
is_first_message = True
keyboard_main = [['Узнать погоду', 'Написать отзыв'],
                 ['Найти ближайшее метро',
                  'Показать аптеки вашего города'],
                 ['Вернуться в начало', 'Ввести новый адрес'], ['Игры']]

keyboard_games = [['Угадай город'],
                  ['Основные функции']]
keyboard = keyboard_main


def main():
    global updater
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text, get_city)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(Filters.text, get_address)],
            3: [MessageHandler(Filters.text, second_start)],
            4: [MessageHandler(Filters.text, get_comments)],
            5: [MessageHandler(Filters.text, text_commands)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    # dp.add_handler(MessageHandler(Filters.text, text_commands))


def start(update, context):
    global user_city
    update.message.reply_text(
        'Введите ваш город и адрес, что бы разблокировать весь функционал бота')
    update.message.reply_text('Введите город',
                              reply_markup=ReplyKeyboardRemove())
    return 1


def get_city(update, context):
    global user_city
    user_city = update.message.text
    update.message.reply_text('Введите адрес')
    return 2


def get_address(update, context):
    global user_address
    user_address = update.message.text
    reply_keyboard = [['/yes', '/no']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Вы правильно всё ввели?', reply_markup=markup)
    return 3


def second_start(update, context):
    global user_city
    update.message.reply_text(f'Ваш город: {user_city}')
    update.message.reply_text(f'Ваш адрес: {user_address}')
    if update.message.text == '/no':
        update.message.reply_text('Введите город')
        return 1
    else:
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text('Выбирете действие',
                                  reply_markup=markup)
    return 5


def get_weather(update, context):
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
    global user_city
    global user_address
    metro_is_near = True
    metro_name = metro(user_city, user_address)[0]
    print(metro(user_city, user_address))
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
            f'Рядом с вами нету метро, да поможет вам бог!')


def get_pharmacy(update, context):
    global user_city
    global user_address
    pharmacy_is_near = True
    print(pharmacy(user_city, user_address))
    try:
        file_name = pharmacy(user_city, user_address)[0]
    except Exception as e:
        pharmacy_is_near = False
    if file_name != 'Рядом с вами нету аптеки' and pharmacy_is_near is True:
        update.message.reply_photo(photo=open(f'img/{file_name}', 'rb'))
    else:
        update.message.reply_text(
            f'Рядом с вами нету аптеки, земля вам пухом!')


def get_comments(update, context):
    global user_comment
    global user_name
    user_comment = update.message.text
    return 5


def text_commands(update, context):
    global user_comment
    global keyboard
    global current_city
    global game_is_played
    print(update.message.text)
    if update.message.text == '/start':
        update.message.reply_text(
            'Введите ваш город и адрес, что '
            'бы разблокировать весь функционал бота')
        update.message.reply_text('Введите город')
        return 1

    if update.message.text == 'Вернуться в начало':
        update.message.reply_text('Введите город')
        return 1

    if update.message.text == 'Ввести новый адрес':
        update.message.reply_text('Введите новый адрес')
        return 2

    if update.message.text == '/exit':
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

    if update.message.text == 'Написать отзыв':
        reply_keyboard = [['/exit']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        update.message.reply_text(
            f'Сюда вы можете написать ваш комментарий', reply_markup=markup)
        return 4

    if update.message.text == 'Узнать погоду':
        get_weather(update, context)

    if update.message.text == 'Найти ближайшее метро':
        get_metro(update, context)

    if update.message.text == 'Показать аптеки вашего города':
        get_pharmacy(update, context)

    if update.message.text == 'Игры':
        keyboard = keyboard_games
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(
            f'Переключаю на клавиатуру "{update.message.text}"',
            reply_markup=markup)

    if update.message.text == 'Основные функции':
        keyboard = keyboard_main
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(
            f'Переключаю на клавиатуру "{update.message.text}"',
            reply_markup=markup)

    if update.message.text == 'Угадай город':
        reply_keyboard = [['/give_up']]
        markup = ReplyKeyboardMarkup(reply_keyboard)
        map_file, current_city = guess_the_city()
        update.message.reply_text(
            f'Напишите названия этого города', reply_markup=markup)
        update.message.reply_photo(
            photo=open(f'img/{map_file}', 'rb'))
        game_is_played = True
        print(current_city)

    if update.message.text == '/give_up':
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(f'Это был город: {current_city}',
                                  reply_markup=markup)
        current_city = ''

    if game_is_played is True:
        if update.message.text == current_city:
            markup = ReplyKeyboardMarkup(keyboard)
            update.message.reply_text(
                f'Правильно! Это был город: {current_city}',
                reply_markup=markup)
        else:
            update.message.reply_text(f'Неверно или ничего не написано')


def stop(update, context):
    update.message.reply_text(
        "Досвидания")
    return ConversationHandler.END  # Константа, означающая конец диалога.


if __name__ == '__main__':
    main()
    updater.start_polling()
    updater.idle()
