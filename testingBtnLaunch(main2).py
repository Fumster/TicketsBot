import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
import configparser
import workWithDB as db

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

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Б":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "В":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Г":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "Д":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "И":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        a = telebot.types.ReplyKeyboardRemove()
        block = block.replace(block, message.text)
        bot.send_message(message.chat.id, "Напишите кабинет", reply_markup=a)

    elif message.text == "К":

        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

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

            room = block + cab

            # Отправка в чат АСУ
            # ---------------------------------------

            markup2 = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(text="Принять", callback_data="accept")
            markup2.add(btn1)

            issuer_msg_id = db.getNewIdForApplication()

            print(issuer_msg_id.__class__)

            bot.send_message(channel_id,
                             f'Новая заявка #{issuer_msg_id}\nАвтор:{message.from_user.username}\nКабинет: {room}\nСодержание:{message.text}',
                             reply_markup=markup2)

            # bot.edit_message_text(
            #     f'⚠️Новая заявка #{issuer_msg_id}\nАвтор:{message.from_user.username}\nКабинет: {room}\nСодержание:{message.text}',
            #     channel_id,
            #     issuer_msg_id, reply_markup=markup2)
            # ---------------------------------

            # bot.edit_message_text(f"заявка #{issuer_msg_id} добавлена", message.chat.id, message.id)

            bot.send_message(message.chat.id, f"заявка #{issuer_msg_id} добавлена")

            db.createNewIssue(channel_id, message.chat.id, message.id, issuer_msg_id, room, message.text)

            bot.send_message(message.chat.id,
                             text="Ожидается следующая заявка".format(
                                 message.from_user), reply_markup=markup)

            cab = cab.replace(cab, "_")
            block = block.replace(block, "_")


@bot.callback_query_handler(func=lambda callback: callback.data == 'accept')
def accept_ticket(callback):
    print("callback.message")
    print(callback.message)
    print("=======================")
    print("callback.from_user")
    print("\n")
    print(callback.from_user)
    content = callback.message.text.split("Содержание:")[1]
    bot.edit_message_text(
        f"🟨заявка #{callback.message.id} в работе - {callback.from_user.username}\nСодержание: {content}",
        channel_id, callback.message.id)
    bot.forward_message(callback.from_user.id, channel_id, callback.message.id)
    db.acceptIssue(callback.message.id, callback.from_user.id)
    # type_answer = callback.data.split("@")[0].split(":")[1]

    # answers = {
    #     "accept": "Принимай трейд",
    #     "not_enough_cases": "Мало кейсов"
    # }
    # text = answers[type_answer]
    bot.send_message(chat_id=callback.from_user.id, text="Это сообщение должен был написать бот тому, кто принял")


bot.polling(none_stop=True)
