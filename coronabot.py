# coding: utf-8

import requests
import telebot
from telebot import types
import config
import strings
import json
import time


# определяем класс заказа пользователя
class FinalStat(object):
    """ Класс Customer: несет всю информацию о заказе пользователя
        Поля:
            confirmed: кол-во зараженных
            deaths:    умершие
            recovered: выздоровили
        Методы:
    """

    def __init__(self, country, date, confirmed, deaths, recovered):
        """Constructor"""
        self.country = country
        self.date = date
        self.confirmed = confirmed
        self.deaths = deaths
        self.recovered = recovered

    def get_stat(self):
        stat_string = \
            "Последние данные по коронавирусу в %s на дату: \n%s\n" % (self.country, self.date) + \
            "Заражено: %s\n" % self.confirmed + \
            "Умерло: %s\n" % self.deaths + \
            "Выздоровление: %s" % self.recovered
        return stat_string


# указываем токен бота
bot = telebot.TeleBot(config.token)


# get_latest_russia_stat получает текущую инфу по России
def get_latest_russia_stat():

    response = requests.request("GET", config.RUSSIA_API_URL)

    decoded_json = json.loads(response.text)
    data = decoded_json["data"]
    date = decoded_json["dt"]

    # print(("Последние данные по коронавирусу по России на дату: %s" % date))
    # print("Зараженные: %s" % data["confirmed"])
    # print("Смерть от короновируса: %s" % data["deaths"])
    # print("Вылечились: %s" % data["recovered"])

    statistic.country = "России"
    statistic.date = date
    statistic.confirmed = data["confirmed"]
    statistic.deaths = data["deaths"]
    statistic.recovered = data["recovered"]

    return 0


# get_latest_russia_stat получает текущую инфу по США
def get_latest_usa_stat():

    response = requests.request("GET", config.USA_API_URL)

    decoded_json = json.loads(response.text)
    data = decoded_json["data"]
    date = decoded_json["dt"]

    statistic.country = "США"
    statistic.date = date
    statistic.confirmed = data["confirmed"]
    statistic.deaths = data["deaths"]
    statistic.recovered = data["recovered"]

    return 0


# get_latest_russia_stat получает текущую инфу по миру
def get_latest_world_stat():
    response = requests.request("GET", config.WORLD_API_URL)

    decoded_json = json.loads(response.text)
    data = decoded_json["data"]
    date = decoded_json["dt"]

    statistic.country = "мире"
    statistic.date = date
    statistic.confirmed = data["confirmed"]
    statistic.deaths = data["deaths"]
    statistic.recovered = data["recovered"]

    return 0


# посылаем курс биткоина пользователю в чат
def send_message_to_user(message):
    # отправляем пользователю сообщение с инфой по короне
    bot.send_message(message.chat.id, statistic.get_stat())
   # start_dlg(message)


def send_msg(message):
    bot.send_message(message.chat.id, strings.msg_info)


# обработчик при старте команды - /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, strings.msg_help)
    # стартовый набор кнопок
    start_dlg(message)


# обработчик при старте команды - /russia - узнать инфо по россии
@bot.message_handler(commands=["russia"])
def rate(message):
    get_latest_russia_stat()
    send_message_to_user(message)


# обработчик при старте команды - /usa - узнать инфо по сша
@bot.message_handler(commands=["usa"])
def rate(message):
    get_latest_usa_stat()
    send_message_to_user(message)


# обработчик при старте команды - /world - узнать инфо по миру
@bot.message_handler(commands=["world"])
def settings(message):
    get_latest_world_stat()
    send_message_to_user(message)


# обработчик при старте команды - /info
@bot.message_handler(commands=["info"])
def start(message):
    bot.send_message(message.chat.id, strings.msg_info)
    # стартовый набор кнопок
    start_dlg(message)


# обработчик при старте команды - /help
@bot.message_handler(commands=["help"])
def start(message):
    bot.send_message(message.chat.id, strings.msg_help)
    # стартовый набор кнопок
    start_dlg(message)


# на любые ответы пользователя в чат бота
# показываем опять главное меню, дабы пользователь только нажимал кнопки диалога
@bot.message_handler(content_types=["text"])
def any_msg(message):
     start_dlg(message)


# при старте бота выводим основные кнопки меню - начало диалога с пользователем
def start_dlg(message):
    # Создаем клавиатуру и каждую из кнопок
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    url_button = types.InlineKeyboardButton(text="Посетите сайт разработчика бота", url=config.my_site_URL)
    info_button = types.InlineKeyboardButton(text="Инфо о коронавирусе COVID-19", callback_data="info")
    callback_button_rus = types.InlineKeyboardButton(text=strings.btn_Russia, callback_data="russia")
    callback_button_usa = types.InlineKeyboardButton(text=strings.btn_USA, callback_data="usa")
    callback_button_world = types.InlineKeyboardButton(text=strings.btn_World, callback_data="world")

    keyboard.add(callback_button_rus, callback_button_usa, callback_button_world, info_button, url_button)

    # bot.send_message(message.chat.id, strings.msg_help)
    bot.send_message(message.chat.id, "Выбирай пункт меню для дальнейших действий:", reply_markup=keyboard)


# ------------------------------------------------------------------------------------------
# главный обработчик всех нажатий пользователя на кнопки диалога, для формирования заказа
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    # Если сообщение из чата с ботом
    if call.message:
        # Если нажата inline-кнопка "Данные по России"
        if call.data == "russia":
            get_latest_russia_stat()
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=statistic.get_stat())
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=statistic.get_stat())
            send_message_to_user(call.message)
            time.sleep(5)
            start_dlg(call.message)

        # Если нажата inline-кнопка "Данные по США"
        if call.data == "usa":
            get_latest_usa_stat()
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=statistic.get_stat())
            send_message_to_user(call.message)
            time.sleep(5)
            start_dlg(call.message)

        # Если нажата inline-кнопка "Данные по миру"
        if call.data == "world":
            get_latest_world_stat()
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=statistic.get_stat())
            send_message_to_user(call.message)
            time.sleep(5)
            start_dlg(call.message)

        # Если нажата inline-кнопка "Информация по коронавирусу"
        if call.data == "info":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=strings.msg_info)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=strings.msg_info)
            time.sleep(5)
            start_dlg(call.message)


# самое основное тут )
if __name__ == '__main__':

    statistic = FinalStat("null", "null", "null", "null", "null")

# делаем так чтобы наш бот не падал когда сервер api.telegram.org выкидывает нашего бота)
    while True:
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(str(e)) # или просто print(e) если у вас логгера нет,
            # или import traceback; traceback.print_exc() для печати полной инфы
            time.sleep(15)

        # чтобы остановить бот по нажатию CTRL-C в терминале
        except KeyboardInterrupt:
            exit()
