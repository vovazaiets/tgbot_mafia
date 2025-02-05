import telebot
from dotenv import load_dotenv
import os
from telebot import InlineKeyboardMarkup,InlineKeyboardButton


load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"hi this is mafia bot")


@bot.message_handler(func=lambda message:True)
def echo_message(message):
    bot.reply_to(message,"не викупив")




bot.infinity_polling()

