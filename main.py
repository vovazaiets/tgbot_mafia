import telebot
from dotenv import load_dotenv
import os
from telebot import types


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot_username= os.getenv("username")
add_bot_url = f"https://t.me/{bot_username}?startgroup=true"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    add_to_group_button = types.InlineKeyboardButton("🤖Додати бота в свій чат",callback_data="addgroup",url=add_bot_url)
    markup.add(add_to_group_button)
    bot.reply_to(message,"hi this is mafia bot",reply_markup=markup)


@bot.message_handler(func=lambda message:True)
def echo_message(message):
    bot.reply_to(message,"не викупив")


# @bot.callback_querry_handler(func=lambda call:True)
# def callback_querry(call):
    # if call.data == 'addgroup':

        


bot.infinity_polling()

