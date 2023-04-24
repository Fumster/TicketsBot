import telebot
from config import *

bot = telebot.TeleBot('5678654199:AAGqvTEHAdXE3mPdkDbc-x6kMkN5Pvqop4w')


@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    bot.reply_to(message, "Hi!")


print("Starting bot")
bot.infinity_polling()
print("End")
