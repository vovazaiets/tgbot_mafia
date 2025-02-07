import telebot
from dotenv import load_dotenv
import os
from telebot import types
import time
import threading
from types import SimpleNamespace
import random

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot_username= os.getenv("username")
add_bot_url = f"https://t.me/{bot_username}?startgroup=true"

bot = telebot.TeleBot(TOKEN)
# list_users = {}
users_id = []
TimeRegestration = 180
interval = 60
list_roles = ["Mafia","Doctor","Normis"]
random.shuffle(list_roles)

REGESTRATION = False
GAME_STARTED = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup()
        add_to_group_button = types.InlineKeyboardButton("🤖Додати бота в свій чат!",callback_data="addgroup",url=add_bot_url)
        markup.add(add_to_group_button)
        bot.reply_to(message,"hi this is mafia bot",reply_markup=markup)
    elif message.chat.type in ["group","supergroup"]:
        print(GAME_STARTED)
        bot.reply_to(message,"Привіт я бот для гри в мафію🤖")



def update_message(message,first_name):
    message += f"\n{first_name}"
    return message

# def send_start(message):
#     # print("func work")
#     bot.send_message(message.chat.id,"/startgame")
# # messageRegestration = f"Починається реєстрація на гру\n"

messageRegestration = f"Починається реєстрація на гру\n"


def update_timer(message, time_left):

    bot.send_message(message.chat.id, f"⏳ До кінця реєстрації залишилось: {time_left} секунд.")

    if time_left > 0:
        threading.Timer(interval, update_timer, [message, time_left - interval]).start()
    else:
        start_game(message)  


@bot.message_handler(commands=['game'])
def start_regestration(message):
    global REGESTRATION
    if REGESTRATION == False:
        if message.chat.type in ["group","supergroup"]:
            global list_players_markup
            global messageRegestration
            messageRegestration = f"Починається реєстрація на гру\n"
            GAME_STARTED = False
            print(GAME_STARTED)
            
            REGESTRATION = True
            list_players_markup = types.InlineKeyboardMarkup()
            list_players_add = types.InlineKeyboardButton("Connect",callback_data="connectgame")
            list_players_markup.add(list_players_add)
            bot.send_message(message.chat.id,messageRegestration,reply_markup=list_players_markup)
            timer_reg = threading.Timer(TimeRegestration,lambda: start_game(message))
            timer_reg.start()
            #bot.send_message(message.chat.id,f"⏳Починається реєстрація на гру,залишилось: {TimeRegestration} секунд")
            update_timer(message, TimeRegestration)
        else:
            bot.reply_to(message,"this is command use in groups")
    elif REGESTRATION == True:
        bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=['startgame'])
def start_game(message):
    global REGESTRATION
    global GAME_STARTED
    global list_roles
    global users_id
    if REGESTRATION == True:
        REGESTRATION = False
        GAME_STARTED = True
        print(GAME_STARTED)
        players_roles = dict(zip(list_roles,users_id))
        print(players_roles)
        for role,player in players_roles.items():
            bot.send_message(player,f"You role is: {role}")
            if role == "Mafia":
                bot.send_message(player,f"Select user to kill: \n\n hehe")
        bot.send_message(message.chat.id, "Гра розпочалась")
        with open("night01.mp4", "rb") as video:
            bot.send_video(message.chat.id, video,timeout=60,caption="🌃 Настає ніч")


    else:
        bot.delete_message(message.chat.id, message.message_id)

@bot.callback_query_handler(func=lambda call:True)
def callback_querry(call):
    print(GAME_STARTED)
    if call.data == 'connectgame':
        # global REGESTRATION
        # global GAME_STARTED
        print(GAME_STARTED)
        if GAME_STARTED == False:
            # REGESTRATION = True
            print(call.from_user.first_name)
            print(call.from_user.id)
            id_user = call.from_user.id
            firstname = call.from_user.first_name
            bot.send_message(id_user,"You join to game")
            if id_user in users_id:
                bot.send_message(id_user,"no no no chill bro,you in game")
            else:
                users_id.append(id_user)
                # list_users[id_user]=None
                global list_players_markup
                global messageRegestration
                messageRegestration = update_message(message=messageRegestration,first_name=firstname)
                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=messageRegestration,reply_markup=list_players_markup)
                # print(list_users[0])
        elif GAME_STARTED == True:
            print("pyk pyk")
       




@bot.message_handler(commands=['stop'])
def stop_game(message):
    global REGESTRATION
    global GAME_STARTED
    if REGESTRATION == True:
        messageRegestration = f"Починається реєстрація на гру\n"
        users_id.clear()
        REGESTRATION = False
        list_players_markup = None
        bot.send_message(message.chat.id,"Registation canceled")
    elif GAME_STARTED == False:
        messageRegestration = f"Починається реєстрація на гру\n"
        users_id.clear()
        bot.delete_message(message.chat.id, message.message_id)
    elif GAME_STARTED == True:
        messageRegestration = f"Починається реєстрація на гру\n"
        users_id.clear()
        GAME_STARTED = False
        bot.send_message(message.chat.id, "Game canceled")
    else:
        print("pyk pyk")

# @bot.message_handler(func=lambda message:True)
# def echo_message(message):
    # bot.reply_to(message,"не викупив")

bot.infinity_polling()

