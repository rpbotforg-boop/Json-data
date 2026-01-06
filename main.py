import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread
from search_engine import format_detailed_result

# --- RENDER WEB SERVICE SUPPORT (DO NOT REMOVE) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running 24/7!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- BOT CONFIGURATION ---
API_ID = 22447622           # Apna API ID dalein
API_HASH = "543b62d58d3e723e766ba57a984ab65d"      # Apna API Hash dalein
BOT_TOKEN = "8523789813:AAGN7UPz54iFcxfdmsHYGMbS3rpmhGEYT8k"    # Apna Bot Token dalein
SUDO_USERS = [777756062]     # Apni Telegram ID dalein
LOG_CHAT_ID = -1003481794992   # Log Group/Channel ID dalein

bot = Client("search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Auth Filter
def is_auth(_, client, message: Message):
    return message.from_user.id in SUDO_USERS
auth_filter = filters.create(is_auth)

@bot.on_message(filters.command("start"))
async def start(client, message):
    if message.from_user.id not in SUDO_USERS:
        return await message.reply_text("🚫 Access Denied! Admin se sampark karein.")
    await message.reply_text(f"👋 **Hii {message.from_user.first_name}!**\nSearch ke liye `/search [Query]` likhein.")

@bot.on_message(filters.command("add") & auth_filter)
async def add_user(client, message):
    try:
        new_id = int(message.command[1])
        if new_id not in SUDO_USERS:
            SUDO_USERS.append(new_id)
            await message.reply_text(f"✅ User `{new_id}` added.")
    except: await message.reply_text("Usage: `/add [User_ID]`")

@bot.on_message(filters.command("broadcast") & auth_filter)
async def broadcast(client, message):
    if not message.reply_to_message: return
    for user in SUDO_USERS:
        try: await message.reply_to_message.copy(user)
        except: pass
    await message.reply_text("📢 Broadcast Done!")

@bot.on_message(filters.command("search") & auth_filter)
async def search_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ Usage: `/search 8601513360`")
    
    query = message.text.split(None, 1)[1]
    
    # Logging Activity
    log_msg = (f"🕵️ **New Search**\n👤 **By:** {message.from_user.first_name}\n"
               f"🆔 **ID:** `{message.from_user.id}`\n🔍 **Query:** `{query}`")
    await client.send_message(LOG_CHAT_ID, log_msg)

    msg = await message.reply_text("🔎 **Searching database...**")
    
    try:
        # NOTE: Yahan apni API connect karein
        # res = requests.get(f"https://your-api.com/api?q={query}").json()
        
        # Testing with Dummy Data
        dummy = {"status": "found", "count": 1, "data": [{"name": "Test User", "fname": "Father Name", "id": "634731473361", "address": "Prayagraj!UP", "mobile": query}]}
        
        report = format_detailed_result(dummy)
        await msg.edit(report, disable_web_page_preview=False)
    except Exception as e:
        await msg.edit(f"❌ Error: `{e}`")

if __name__ == "__main__":
    print("🚀 Starting Web Server...")
    keep_alive()  # Flask ko background thread mein start karega
    
    print("🤖 Starting Telegram Bot...")
    bot.run()     # Bot ko main thread mein rakhega


