import telebot
from dotenv import load_dotenv
import os
from telebot import types
import threading
import random
from config import TimeRegestration,interval,list_roles,chatonly_id

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot_username= os.getenv("username")
add_bot_url = f"https://t.me/{bot_username}?startgroup=true"
players_roles = {}
bot = telebot.TeleBot(TOKEN)
users_id = []

class Game:
    REGISTRATION = False
    GAME_STARTED = False
    messageRegistration = f"Починається реєстрація на гру\n"
    def Change_status(reg=None,game_started=None):
        if reg:
            Game.REGISTRATION = True
        elif game_started:
            Game.GAME_STARTED = True
        elif not game_started:
            Game.GAME_STARTED = False
        elif not reg:
            Game.REGISTRATION = False
        else:
            pass
        
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        markup = types.InlineKeyboardMarkup()
        add_to_group_button = types.InlineKeyboardButton("🤖Додати бота в свій чат!",callback_data="addgroup",url=add_bot_url)
        markup.add(add_to_group_button)
        bot.reply_to(message,"Привіт я бот для гри в мафію🤖",reply_markup=markup)
    elif message.chat.type in ["group","supergroup"]:
        bot.reply_to(message,"Привіт я бот для гри в мафію🤖")

def update_message(message,first_name):
    message += f"\n{first_name}"
    return message

def update_timer(message, time_left):
    if time_left > 0:
        if Game.GAME_STARTED == False:
            bot.send_message(message.chat.id, f"⏳ До кінця реєстрації залишилось: {time_left} секунд.")
            threading.Timer(interval, update_timer, [message, time_left - interval]).start()
        else:
            print("pyk pyk")
    else:
        start_game(message)  


@bot.message_handler(commands=['game'])
def start_regestration(message):
    if Game.REGISTRATION == False:
        if message.chat.type in ["group","supergroup"]:
            global list_players_markup
            Game.GAME_STARTED = False
            Game.REGISTRATION = True
            list_players_markup = types.InlineKeyboardMarkup()
            list_players_add = types.InlineKeyboardButton("Приєднатись до гри",callback_data="connectgame")
            list_players_markup.add(list_players_add)
            bot.send_message(message.chat.id,Game.messageRegistration,reply_markup=list_players_markup)
            timer_reg = threading.Timer(TimeRegestration,lambda: start_game(message))
            timer_reg.start()
            update_timer(message, TimeRegestration)
        else:
            bot.reply_to(message,"Цю команду можна використати тільки в групі!")
    elif Game.REGISTRATION == True:
        bot.delete_message(message.chat.id, message.message_id)



def send_message_by_id(user_id,text):
    bot.send_message(user_id,text)

def func_mafia(user_id,players_roles):
    markup_mafia = types.InlineKeyboardMarkup()
    for player in users_id:
        user_info = bot.get_chat(player)
        button = types.InlineKeyboardButton(text=f"{user_info.first_name}",callback_data=f"kill_{player}")
        markup_mafia.add(button)
    button_pass = types.InlineKeyboardButton(text="🏳️Утриматись",callback_data="pass_mafia_kill")
    markup_mafia.add(button_pass)
    bot.send_message(user_id,f"🔪Ти обрав жертву:\n",reply_markup=markup_mafia)

def day(player):
    global users_id
    list_live_user = ""
    if player != 0:
        users_id.pop()

    if not users_id:
        bot.send_message(chatonly_id,"Гра закінчилась\nПереможець: Мафія")
        Game.GAME_STARTED = False
        Game.REGISTRATION = False
    else:
        for player in users_id:
            list_live_user += f"{bot.get_chat(player).first_name}\n"
        bot.send_message(chatonly_id,f"Лишились в живих:\n\n{list_live_user}")
        func_mafia(player,players_roles)

@bot.callback_query_handler(func=lambda call: call.data.startswith("kill_"))
def kill_player(call):
    global players_roles
    player_id = call.data.split("_")[1]
    role = call.data.split("_")[0]
    bot.send_message(player_id,text=f"You selected kill player {bot.get_chat(player_id).first_name}")
    bot.send_message(chatonly_id,f"Мафія вибрала жертву")
    # del players_roles[f'{role}']
    day(player_id)

@bot.message_handler(commands=['startgame'])
def start_game(message):
    global players_roles
    global list_roles
    global users_id
    if Game.REGISTRATION:
        # Game.REGISTRATION = False
        # Game.GAME_STARTED = True
        Game.Change_status(1,0)
        random.shuffle(list_roles)
        players_roles = dict(zip(list_roles,users_id))
        print(players_roles)
        for role,player in players_roles.items():
            bot.send_message(player,f"Маєш файну роль: {role}")
            if role == "Mafia":
                # send_message_by_id(player,"SELECT")
                # bot.send_message(player,f"Select user to kill: \n\n hehe")
                func_mafia(player,players_roles)
                
        bot.send_message(message.chat.id, "Гра розпочалась")
        with open("night01.mp4", "rb") as video:
            bot.send_video(message.chat.id, video,timeout=60,caption="🌃 Настає ніч")


    else:
        bot.delete_message(message.chat.id, message.message_id)

@bot.callback_query_handler(func=lambda call:True)
def callback_querry(call):
    if call.data == 'connectgame':
        if Game.GAME_STARTED == False:
            print(call.from_user.first_name)
            print(call.from_user.id)
            id_user = call.from_user.id
            firstname = call.from_user.first_name
            bot.send_message(id_user,"Ти приєднався до гри в мафію!")
            if id_user in users_id:
                bot.send_message(id_user,"Не треба так :)")
            else:
                users_id.append(id_user)
                global list_players_markup
                Game.messageRegistration = update_message(message=Game.messageRegistration,first_name=firstname)
                bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=Game.messageRegistration,reply_markup=list_players_markup)
        elif Game.GAME_STARTED == True:
            print("pyk pyk")
    elif call.data == 'pass_mafia_kill':
        bot.send_message(chatonly_id,"Мафія вирішила утриматись")
        day(0)

@bot.message_handler(commands=['stop'])
def stop_game(message):
    if Game.REGISTRATION:
        Game.messageRegistration = f"Починається реєстрація на гру\n"
        users_id.clear()
        Game.REGISTRATION = False
        list_players_markup = None
        bot.send_message(message.chat.id,"Реєстрацію скасовано")
    elif not Game.GAME_STARTED:
        Game.messageRegistration = f"Починається реєстрація на гру\n"
        users_id.clear()
        bot.delete_message(message.chat.id, message.message_id)
    elif Game.GAME_STARTED:
        Game.messageRegistration = f"Починається реєстрація на гру\n"
        users_id.clear()
        Game.GAME_STARTED = False
        bot.send_message(message.chat.id, "Гру скасовано")
    else:
        print("pyk pyk")

bot.infinity_polling()