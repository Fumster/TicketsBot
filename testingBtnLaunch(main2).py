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
id_experiment = 0
issue_msg_id = "_"
closing = False


# Начало работы
@bot.message_handler(commands=['start'])
def start(message):
    # Инициализация кнопок
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("➕ Добавить заявку")
    btn2 = types.KeyboardButton("❓ Информация о боте")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id,
                     text="Вас приветствует бот для подачи заявок АСУ".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global block
    global cab
    global closing
    global issue_msg_id

    # Добавление заявки
    if message.text == "➕ Добавить заявку":

        # bot.delete_message(message.chat.id, message.id-2)
        # bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        # bot.edit_message_text("заявка должна быть не менее 10 символов", message.chat.id, message.id-2)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btns = []

        for e in blocks:
            btns.append(types.KeyboardButton(e))
        btns.append(types.KeyboardButton("Назад"))

        markup.add(*btns)

        bot.send_message(message.chat.id, text="Выберите блок", reply_markup=markup)

    # информация о боте
    elif message.text == "❓ Информация о боте":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("Назад")
        markup.add(back)
        bot.send_message(message.chat.id, text="Данный бот создан для подачи заявок в АСУ", reply_markup=markup)



    # Обработка блоков
    # -----------------------------------------------------
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
    # -----------------------------------------------------

    # кнопка назад
    elif message.text == "Назад":

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("➕ Добавить заявку")
        button2 = types.KeyboardButton("❓ Информация о боте")
        markup.add(button1, button2)
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, text="Главное меню", reply_markup=markup)

    # ----------------------------------------------------------------------------

    else:

        if block == '_' and cab == '_':

            # Закрытие заявки
            if closing:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton("➕ Добавить заявку")
                button2 = types.KeyboardButton("❓ Информация о боте")
                markup.add(button1, button2)

                # bot.send_message(message.chat.id,
                #                  text=f"☑Заявка {issue_msg_id} закрыта\nРешение: {message.text}".format(
                #                      message.from_user), reply_markup=markup)

                content = db.getContent(issue_msg_id)

                id_experiment = db.getBotAcceptId(issue_msg_id)

                bot.edit_message_text(
                    f"☑️заявка #{issue_msg_id} закрыта - {message.from_user.username}\n--{content}--\nРешение:{message.text}",
                      message.chat.id, id_experiment)

                bot.edit_message_text(
                    f"☑️заявка #{issue_msg_id} закрыта - {message.from_user.username}\n--{content}--\nРешение:{message.text}",
                      channel_id, issue_msg_id)


                closing = False

                bot.delete_message(message.chat.id, message.id - 1)
                bot.delete_message(message.chat.id, message.id)

                db.closeApplications(issue_msg_id, message.from_user.id, message.text)

                issue_msg_id = issue_msg_id.replace(issue_msg_id, "_")


            # Обработка неизвестных команд
            else:
                bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован..")

        # Создание новой заявки
        elif block != '_' and cab == '_':

            # Ввод номера кабинета
            bot.delete_message(message.chat.id, message.id - 1)
            bot.delete_message(message.chat.id, message.id)

            # Проверка номера кабинета
            if message.text.isdigit():
                cab = cab.replace(cab, message.text)
                bot.send_message(message.chat.id, text="Опишите проблему")
            else:
                bot.send_message(message.chat.id,
                                 f"Не правильный формат номера кабинета кабинета, должны содержаться только числа")
        else:
            # Ввод описания проблемы
            bot.delete_message(message.chat.id, message.id - 1)
            bot.delete_message(message.chat.id, message.id)

            # Возвращение к изначальному меню
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("➕ Добавить заявку")
            button2 = types.KeyboardButton("❓ Информация о боте")
            markup.add(button1, button2)

            # Формирование кабинета
            room = block + cab

            # Отправка в чат АСУ
            # ---------------------------------------
            markup2 = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(text="Принять", callback_data="accept")
            markup2.add(btn1)
            issuer_msg_id = bot.send_message(channel_id,
                                      'Н',
                                      reply_markup=markup2).id

            bot.edit_message_text(
                f'⚠️Новая заявка #{issuer_msg_id}\nАвтор:{message.from_user.username}\nСодержание:{message.text}',
                channel_id,
                issuer_msg_id, reply_markup=markup2)
            # ---------------------------------

            bot.send_message(message.chat.id, f"заявка #{issuer_msg_id} добавлена", reply_markup=markup)

            db.createNewIssue(channel_id, message.chat.id, message.id, issuer_msg_id, room, message.text)


            cab = cab.replace(cab, "_")
            block = block.replace(block, "_")


@bot.callback_query_handler(func=lambda callback: callback.data == 'accept')
def accept_ticket(callback):

    content = callback.message.text.split("Содержание:")[1]

    bot.edit_message_text(
        f"🟨заявка #{callback.message.id} в работе - {callback.from_user.username}\nСодержание: {content}",
        channel_id, callback.message.id)

    markup2 = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Закрыть", callback_data=f"close-{callback.message.id}")
    markup2.add(btn1)

    id = bot.send_message(chat_id=callback.from_user.id,
                     text=f"🟨 Вы приняли заявку #{callback.message.id}\nСодержание: {content}", reply_markup=markup2).id

    # bot.forward_message(callback.from_user.id, channel_id, callback.message.id)

    db.acceptIssue(callback.message.id, callback.from_user.id, id)
    # type_answer = callback.data.split("@")[0].split(":")[1]

    # answers = {
    #     "accept": "Принимай трейд",
    #     "not_enough_cases": "Мало кейсов"
    # }
    # text = answers[type_answer]
    # bot.send_message(chat_id=callback.from_user.id, text="Это сообщение должен был написать бот тому, кто принял")


@bot.callback_query_handler(func=lambda callback: 'close' in callback.data)
def closingIssueHandler(callback):
    global issue_msg_id
    global closing
    global id_experiment

    issue_msg_id = issue_msg_id.replace(issue_msg_id, callback.data.split("-")[1])

    print(issue_msg_id, db.getOpenerMsgId(issue_msg_id))

    closing = True
    # a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id=callback.from_user.id,text = "Напишите решение")
    return


bot.polling(none_stop=True)
# bot.infinity_polling(timeout=10, long_polling_timeout=5)
