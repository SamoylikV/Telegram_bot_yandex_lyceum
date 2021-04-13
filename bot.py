from telegram.ext import *
from telegram import *
from other.weather import weather
from other.comments import comments
from maps.metro import metro
from maps.pharmacy import pharmacy
from maps.closest_mac import closest_mac
from games.guess_the_city import guess_the_city

# TODO: расписать файлы с нужными функциями------------------------------------
# TODO: получаем город пользователя, и выдаём ему погоду ----------------------
# TODO: показываем карту города, и просим его угадать--------------------------
# TODO: найти ближайшую станцию метро, дистанция до неё -----------------------
# TODO: найти ближайшую аптеку тоже из задачи ---------------------------------
# TODO: написать юнит тесты
# TODO: сделать всё красиво по файлам------------------------------------------
# TODO: Сделать клавиаутуру у пользователя что бы всё тоже было красиво--------
# TODO: ну и коменты расписать

f = open("token.txt", encoding="utf8")
updater = Updater(f.readlines()[0])
try:
    p = open("pass.txt", encoding="utf8")
    admin_pass = p.readlines()[0]
except Exception:
    admin_pass = 'Vasiliy_Samoylik_bhe_best_person_on_the_Earth'

user_name = ''
user_city = ''
user_address = ''
user_comment = ''
user_answer = ''
current_city = ''
try_counter = 0
game_is_played = False
is_admin = True
keyboard_main = [['Узнать погоду', 'Написать отзыв', 'Ввести новый адрес', ],
                 ['Найти ближайшее метро', 'Найти ближайший макдональдс',
                  'Показать центральные аптеки вашего города'],
                 ['Игры']]
keyboard_games = [['Угадай город'],
                  ['Основные функции']]
keyboard_admin = [['Перезапустить бота']]
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
    """
    Приветствуем пользователя и просим ввести его данные о геолокации
    """
    global user_city
    global is_admin
    if is_admin is True:
        update.message.reply_text(
            'Введите ваш город и адрес, '
            'чтобы разблокировать весь функционал бота')
        is_admin = False
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
    if update.message.text == '/no':
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
    except Exception as e:
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
    if update.message.text == 'Ввести новый адрес':
        update.message.reply_text('Введите город')
        return 1

    # Ввод отзыва
    if update.message.text == 'Написать отзыв':
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

    # Обрабтока команды вывода погоды
    if update.message.text == 'Узнать погоду':
        get_weather(update, context)

    # Обрабтока команды вывода метро
    if update.message.text == 'Найти ближайшее метро':
        get_metro(update, context)

    # Обрабтока команды вывода аптек города
    if update.message.text == 'Показать центральные аптеки вашего города':
        get_pharmacy(update, context)

    # Обрабтока команды вывода ближайшего макдональдса
    if update.message.text == 'Найти ближайший макдональдс':
        get_closest_mac(update, context)

    # Обрабтока команды на смены клавиатуры на игровую
    if update.message.text == 'Игры':
        keyboard = keyboard_games
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(
            f'Переключаю на клавиатуру "{update.message.text}"',
            reply_markup=markup)

    # Обрабтока команды на смены клавиатуры на основную
    if update.message.text == 'Основные функции':
        keyboard = keyboard_main
        markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text(
            f'Переключаю на клавиатуру "{update.message.text}"',
            reply_markup=markup)

    # Обрабтока команды на начало игры "Угадай город"
    if update.message.text == 'Угадай город':
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
            update.message.reply_text('Перезапускаю', reply_markup=markup)
            start(update, context)
        else:
            update.message.reply_text('Кажется вы не админ',
                                      reply_markup=markup)


def stop(update, context):
    update.message.reply_text(
        "До свидания")
    return ConversationHandler.END  # Константа, означающая конец диалога.


if __name__ == '__main__':
    main()
    updater.start_polling()
    updater.idle()
