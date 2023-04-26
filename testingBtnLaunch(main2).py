import time

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
import configparser

blocks = ["А", "Б", "В", "Г", "Д", "И", "К"]
config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["Bot"]["token"])

channel_id = config["Bot"]["channel_id"]

block = "_"
cab = "_"

# Начало работы
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("➕ Добавить заявку")
    btn2 = types.KeyboardButton("❓ Информация о боте")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот для твоей статьи для habr.com ".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global block
    global cab
    if message.text == "➕ Добавить заявку":

        # bot.delete_message(message.chat.id, message.id-2)
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        # bot.edit_message_text("заявка должна быть не менее 10 символов", message.chat.id, message.id-2)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btns = []

        for e in blocks:
            btns.append(types.KeyboardButton(e))
        btns.append(types.KeyboardButton("Назад"))

        markup.add(*btns)

        bot.send_message(message.chat.id, text="Выберите блок", reply_markup=markup)

    elif message.text == "❓ Информация о боте":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Назад")
        markup.add(back)
        bot.send_message(message.chat.id, text="Данный бот создан для подачи заявок в АСУ", reply_markup=markup)

    elif message.text == "А":
        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Б":
        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "В":
        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Г":
        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Д":
        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "И":
        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "К":
        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Назад":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("➕ Добавить заявку")
        button2 = types.KeyboardButton("❓ Информация о боте")
        markup.add(button1, button2)
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, text="Главное меню", reply_markup=markup)
    else:
        if block == '_' and cab == '_':
            bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")
        elif block != '_' and cab == '_':
            bot.delete_message(message.chat.id, message.id - 1)
            bot.delete_message(message.chat.id, message.id)
            cab = cab.replace(cab, message.text)
            bot.send_message(message.chat.id, text="Опишите проблему")
        else:
            bot.delete_message(message.chat.id, message.id - 1)
            bot.delete_message(message.chat.id, message.id)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("➕ Добавить заявку")
            button2 = types.KeyboardButton("❓ Информация о боте")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, text=f"{block}{cab} проблема {message.text}", reply_markup=markup)

            cab = cab.replace(cab, "_")
            block = block.replace(block, "_")
bot.polling(none_stop=True)
