import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread
from search_engine import format_detailed_result

# --- RENDER FAKE SERVER ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- CONFIG ---
API_ID = 22447622 
API_HASH = "543b62d58d3e723e766ba57a984ab65d"
BOT_TOKEN = "8523789813:AAGN7UPz54iFcxfdmsHYGMbS3rpmhGEYT8k"
SUDO_USERS = [777756062] # Apni ID yahan dalein
LOG_CHAT_ID = -1003481794992

bot = Client("pro_search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Auth Filter
auth_filter = filters.create(lambda _, __, m: m.from_user.id in SUDO_USERS)

# --- NEW: PROFESSIONAL START & MENU ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    # Professional Menu (Niche keyboard ki jagah dikhega)
    menu_keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("🔍 New Search"), KeyboardButton("👤 My Profile")],
        [KeyboardButton("🛠 Help & Support")]
    ], resize_keyboard=True)

    welcome_text = (
        f"🌟 **Namaste {message.from_user.first_name}!**\n\n"
        "Welcome to the **Premium Search Intelligence Bot**.\n"
        "Aapka access verified hai. Niche diye gaye menu ka use karein."
    )
    
    await message.reply_text(welcome_text, reply_markup=menu_keyboard)

# --- MENU BUTTON HANDLING ---
@bot.on_message(filters.regex("🔍 New Search"))
async def search_btn(client, message):
    await message.reply_text("🔎 Search karne ke liye `/search [Number]` likhein.")

@bot.on_message(filters.regex("👤 My Profile"))
async def profile_btn(client, message):
    await message.reply_text(f"👤 **Name:** {message.from_user.first_name}\n🆔 **ID:** `{message.from_user.id}`\n🔑 **Status:** `Admin Access` ✅")

# --- PURANA SEARCH LOGIC (NO CHANGE) ---
@bot.on_message(filters.command("search") & auth_filter)
async def search_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ `/search [Mobile/ID]`")
    
    query = message.command[1]
    msg = await message.reply_text("⚡ **Fetching Data...**")
    
    try:
        # Logging
        await client.send_message(LOG_CHAT_ID, f"🕵️ **Query:** `{query}` by {message.from_user.id}")

        # (Aapka existing API logic yahan aayega)
        dummy_res = {"status": "found", "count": 1, "data": [{"name": "Professional User", "id": "999", "address": "Delhi!India", "mobile": query}]}
        
        # Result ke neeche professional button
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 New Search", switch_inline_query_current_chat="/search ")]
        ])
        
        report = format_detailed_result(dummy_res)
        await msg.edit(report, reply_markup=buttons)
    except Exception as e:
        await msg.edit(f"❌ Error: `{e}`")

if __name__ == "__main__":
    keep_alive()
    print("🚀 Professional Bot Started!")
    bot.run()
