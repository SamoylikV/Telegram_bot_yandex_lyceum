from telegram.ext import *
from telegram import *
from other_api.weather import weather
from maps.metro import metro
from maps.pharmacy import pharmacy
import random

# TODO: расписать файлы с нужными функциями
# TODO: получаем город пользователя, и выдаём ему погоду ----------------------
# TODO: показываем карту города, и просим его угадать (Можно взять из задачи)
# TODO: найти ближайшую станцию метро, дистанция до неё -----------------------
# TODO: найти ближайшую аптеку тоже из задачи
# TODO: попробовать что нибудь с новостями придумать https://pypi.org/project/GoogleNews/
# TODO: сделать всё красиво по файлам
# TODO: Сделать клавиаутуру у пользователя что бы всё тоже было красиво
# TODO: ну и коменты расписать

f = open("token.txt", encoding="utf8")
updater = Updater(f.readlines()[0])

user_city = ''
user_address = ''


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
            4: [MessageHandler(Filters.text, text_commands)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("get_weather", get_weather))
    # dp.add_handler(MessageHandler(Filters.text, text_commands))


def start(update, context):
    global user_city
    update.message.reply_text(
        'Введите ваш город и адрес, что бы разблокировать весь функционал бота')
    update.message.reply_text('Введите город')
    return 1


def get_city(update, context):
    global user_city
    user_city = update.message.text
    update.message.reply_text('Введите адрес')
    return 2


def get_address(update, context):
    global user_address
    user_address = update.message.text
    reply_keyboard = [['/next']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Продолжить?', reply_markup=markup)
    return 3


def second_start(update, context):
    global user_city
    update.message.reply_text(
        f'Ваш город: {user_city}, ваш адрес: {user_address}')
    reply_keyboard = [['Узнать погоду'], ['Найти ближайшее метро'],
                      ['Найти ближайшее аптеку']]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    update.message.reply_text('Выбирете действие',
                              reply_markup=markup)
    return 4


def get_weather(update, context):
    global user_city
    update.message.reply_text(
        f'В городе {user_city} {weather(user_city)["conditions"]}')
    update.message.reply_text(f'Температура: {weather(user_city)["temp"]}C')


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
        to_pharmacy_distance = pharmacy(user_city, user_address)[1]
    except Exception as e:
        pharmacy_is_near = False
    if file_name != 'Рядом с вами нету аптеки' and pharmacy_is_near is True:
        update.message.reply_photo(photo=open(f'img/{file_name}', 'rb'))
        update.message.reply_text(
            f'Расстояние до аптеки: {to_pharmacy_distance}м')
    else:
        update.message.reply_text(
            f'Рядом с вами нету аптеки, земля вам пухом!')


# def to_ring(context):
#     cont = context.job.context
#     context.bot.send_message(cont[0], text=cont[1])


# def dice(update, context):
#     reply_keyboard = [['кинуть один шестигранный кубик',
#                        'кинуть 2 шестигранных кубика одновременно'],
#                       ['кинуть 20-гранный кубик', 'вернуться назад']]
#     markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
#
#     update.message.reply_text('Как кинуть кубик?',
#                               reply_markup=markup)


def timer(update, context):
    reply_keyboard = [['30 секунд', '1 минута'],
                      ['5 минут', 'вернуться назад']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    update.message.reply_text('Сколько засечь?',
                              reply_markup=markup)


def text_commands(update, context):
    string = None
    print(update.message.text)
    if update.message.text == 'Узнать погоду':
        get_weather(update, context)
    if update.message.text == 'Найти ближайшее метро':
        get_metro(update, context)
    if update.message.text == 'Найти ближайшее аптеку':
        get_pharmacy(update, context)
    # if string:
    #     update.message.reply_text(string)


def stop(update, context):
    update.message.reply_text(
        "Досвидания")
    return ConversationHandler.END  # Константа, означающая конец диалога.


if __name__ == '__main__':
    main()
    updater.start_polling()
    updater.idle()
