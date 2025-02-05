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
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup()
        add_to_group_button = types.InlineKeyboardButton("🤖Додати бота в свій чат",callback_data="addgroup",url=add_bot_url)
        markup.add(add_to_group_button)
        bot.reply_to(message,"hi this is mafia bot",reply_markup=markup)
    elif message.chat.type in ["group","supergroup"]:
        bot.reply_to(message,"Привіт я бот для гри в мафію🤖")


list_users = []

def update_message(message,first_name):
    message += f"\n{first_name}"
    return message


messageRegestration = f"Починається реєстрація на гру\n"

list_players_markup = types.InlineKeyboardMarkup()

@bot.message_handler(commands=['game'])
def start_regestration(message):
    if message.chat.type in ["group","supergroup"]:
        global list_players_markup
        # list_players_markup = types.InlineKeyboardMarkup()
        list_players_add = types.InlineKeyboardButton("Connect",callback_data="connectgame")
        list_players_markup.add(list_players_add)
        bot.send_message(message.chat.id,messageRegestration,reply_markup=list_players_markup)
    else:
        bot.reply_to(message,"this is command use in groups")


@bot.message_handler(func=lambda message:True)
def echo_message(message):
    bot.reply_to(message,"не викупив")


@bot.callback_query_handler(func=lambda call:True)
def callback_querry(call):
    if call.data == 'connectgame':
        print(call.from_user.first_name)
        print(call.from_user.id)
        id_user = call.from_user.id
        firstname = call.from_user.first_name
        bot.send_message(id_user,"You join to game")
        list_users.append(firstname)
        global list_players_markup
        global messageRegestration
        messageRegestration = update_message(message=messageRegestration,first_name=firstname)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=messageRegestration,reply_markup=list_players_markup)
        print(list_users[0])





bot.infinity_polling()

