import telebot
from dotenv import load_dotenv
import os
from telebot import types
import time


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot_username= os.getenv("username")
add_bot_url = f"https://t.me/{bot_username}?startgroup=true"

bot = telebot.TeleBot(TOKEN)
list_users = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup()
        add_to_group_button = types.InlineKeyboardButton("🤖Додати бота в свій чат",callback_data="addgroup",url=add_bot_url)
        markup.add(add_to_group_button)
        bot.reply_to(message,"hi this is mafia bot",reply_markup=markup)
    elif message.chat.type in ["group","supergroup"]:
        bot.reply_to(message,"Привіт я бот для гри в мафію🤖")



def update_message(message,first_name):
    message += f"\n{first_name}"
    return message


messageRegestration = f"Починається реєстрація на гру\n"

list_players_markup = types.InlineKeyboardMarkup()

REGESTRATION = False
GAME_STARTED = False

@bot.message_handler(commands=['game'])
def start_regestration(message):
    global REGESTRATION
    if REGESTRATION == False:
        if message.chat.type in ["group","supergroup"]:
            global list_players_markup
            REGESTRATION = True
            # list_players_markup = types.InlineKeyboardMarkup()
            list_players_add = types.InlineKeyboardButton("Connect",callback_data="connectgame")
            list_players_markup.add(list_players_add)
            bot.send_message(message.chat.id,messageRegestration,reply_markup=list_players_markup)
            bot.send_message(message.chat.id,"До кінця реєстрації залишилось: <time>")
        else:
            bot.reply_to(message,"this is command use in groups")
    elif REGESTRATION == True:
        bot.send_message(message.chat.id,"Regestration started")



@bot.callback_query_handler(func=lambda call:True)
def callback_querry(call):
    if call.data == 'connectgame':
        REGESTRATION = True
        print(call.from_user.first_name)
        print(call.from_user.id)
        id_user = call.from_user.id
        firstname = call.from_user.first_name
        bot.send_message(id_user,"You join to game")
        if firstname in list_users:
            bot.send_message(id_user,"no no no chill bro,you in game")
        else:
            list_users.append(firstname)
            global list_players_markup
            global messageRegestration
            messageRegestration = update_message(message=messageRegestration,first_name=firstname)
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=messageRegestration,reply_markup=list_players_markup)
            print(list_users[0])
       

@bot.message_handler(commands=['startgame'])
def start_game(message):
    if REGESTRATION == True:
        REGESTRATION = False
        GAME_STARTED = True
        bot.send_message(message.chat.id, "Гра розпочалась")
    else:
        bot.reply_to(message.chat.id, ":)")


@bot.message_handler(commands=['stop'])
def stop_game(message):
    REGESTRATION = False
    GAME_STARTED = False
    bot.send_message(message.chat.id, "Гру скасовано")

# @bot.message_handler(func=lambda message:True)
# def echo_message(message):
    # bot.reply_to(message,"не викупив")

bot.infinity_polling()

