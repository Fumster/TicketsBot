import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException
import configparser
import workWithDB as db

config = configparser.ConfigParser()
config.read("settings.ini")

channel_id = config["Bot"]["channel_id"]

def initialise_bot():
    bot = telebot.TeleBot(config["Bot"]["token"])  # test comment

    @bot.message_handler(commands=['add'])
    def add_command_handler(message):
        # удаляем сообщение пользователя с командой /add
        bot.delete_message(message.chat.id, message.id)
        send = bot.send_message(message.chat.id, 'Добавь заявку:')
        bot.register_next_step_handler(send, add_issue, send)
        bot.send_message(chat_id=message.from_user.id, text="Это сообщение должен был написать лично бот")


    def add_issue(message, info_msg):
        print("message")
        print(message)
        print("\n")
        print("--------------------------")
        print("\n")
        print("info_msg")
        print(info_msg)
        print("\n")

        bot.delete_message(message.chat.id, message.id)
        if len(message.text) < 10:
            bot.edit_message_text("заявка должна быть не менее 10 символов", info_msg.chat.id, info_msg.id)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton(text="Принять", callback_data="accept")
            markup.add(btn1)
            issuer_msg_id = bot.send_message(channel_id,
                                      f'Новая заявка #XXX\nАвтор:{message.from_user.username}\nСодержание:{message.text}',
                                      reply_markup=markup).id
            bot.edit_message_text(
                f'⚠️Новая заявка #{issuer_msg_id}\nАвтор:{message.from_user.username}\nСодержание:{message.text}', channel_id,
                issuer_msg_id, reply_markup=markup)
            bot.edit_message_text(f"заявка #{issuer_msg_id} добавлена", info_msg.chat.id, info_msg.id)
            room = "310A"
            db.createNewIssue(channel_id, info_msg.chat.id, info_msg.id,issuer_msg_id,room,message.text)

    @bot.message_handler(commands=['close'])
    def close_handler(message):
        bot.delete_message(message.chat.id, message.id)
        send = bot.send_message(message.chat.id,
                                'Введи номер заявки и решение в формате\n№-решение !тире в тексте решения не допускается!:')
        bot.register_next_step_handler(send, close_issue, send)

    def close_issue(message, info_msg):
        # bot.delete_message(info_msg.chat.id, info_msg.id)
        try:
            number = message.text.split("-")[0]
            resolve = message.text.split("-")[1]
            bot.delete_message(message.chat.id, message.id)
            msg_id = int(number)
        except ValueError:
            bot.edit_message_text("ID заявки должен содержать только цифры", info_msg.chat.id, info_msg.id)
            return
        except IndexError:
            bot.edit_message_text("Неверный формат", info_msg.chat.id, info_msg.id)
            return

        ch_message = bot.forward_message(message.chat.id, channel_id, msg_id)
        bot.delete_message(message.chat.id, ch_message.id)
        content = ch_message.text.split("Содержание: ")[1]
        try:
            bot.edit_message_text(
                f"☑️заявка #{msg_id} закрыта - {message.from_user.username}\n--{content}--\nРешение:{resolve}",
                channel_id, msg_id)
        except ApiTelegramException as e:
            print(e)
            bot.send_message(message.chat.id, "заявка не найдена")
        bot.edit_message_text(f"заявка #{msg_id} закрыта", info_msg.chat.id, info_msg.id)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):

        if not message.text == "add" or "close":
            bot.send_message(message.from_user.id, 'Неизвестная команда')  # ответ бота

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
        db.acceptIssue(callback.message.id,callback.from_user.id)
        # type_answer = callback.data.split("@")[0].split(":")[1]

        # answers = {
        #     "accept": "Принимай трейд",
        #     "not_enough_cases": "Мало кейсов"
        # }
        # text = answers[type_answer]
        bot.send_message(chat_id=callback.from_user.id, text="Это сообщение должен был написать бот тому, кто принял")

    # bot.polling(none_stop=True, interval=0)
    bot.infinity_polling(timeout=10, long_polling_timeout=5)


if __name__ == '__main__':
    print("bot start")
    initialise_bot()
