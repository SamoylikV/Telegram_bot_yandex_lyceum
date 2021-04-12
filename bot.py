from telegram.ext import *
from telegram import *
from maps.geocoder_requests import weather
import random

# TODO: расписать файлы с нужными функциями
# TODO: получаем город пользователя, и выдаём ему погоду
# TODO: показываем карту города, и просим его угадать (Можно взять из задачи)
# TODO: найти ближайшую станцию метро
# TODO: найти ближайшую аптеку тоже из задачи
# TODO: попробовать что нибудь с новостями придумать https://pypi.org/project/GoogleNews/
# TODO: сделать всё красиво по файлам
# TODO: Сделать клавиаутуру у пользователя что бы всё тоже было красиво
# TODO: ну и коменты расписать

updater = Updater("1798521468:AAHuTQmwNVlg1t3mO0vkX7AxFLwUhi-fmSc")

user_city = ''


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
            2: [MessageHandler(Filters.text, second_start)]
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
        'Введите ваш город, что бы разблокировать весь функционал бота')
    return 1


def get_city(update, context):
    global user_city
    user_city = update.message.text
    update.message.reply_text(user_city)
    return 2


def second_start(update, context):
    global user_city
    update.message.reply_text(f'Ваш город: {user_city}')
    reply_keyboard = [['/get_weather']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Выбирете действие',
                              reply_markup=markup)


def get_weather(update, context):
    global user_city
    # update.message.reply_text('Напишите свой город')
    update.message.reply_text(
        f'В городе {user_city} {weather(user_city)["conditions"]}\n'
        f'Температура: {weather(user_city)["temp"]}C')


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
    # if update.message.text == 'Узнать погоду':
    #     start(update, context)
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
