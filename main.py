import os
import requests
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
from threading import Thread
from search_engine import format_detailed_result

# --- RENDER WEB SUPPORT (24/7) ---
app = Flask(__name__)
@app.route('/')
def home(): return "🔥 Deep Search Bot is Online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- CONFIGURATION ---
API_ID = 22447622           # Apna API ID yahan dalein
API_HASH = "543b62d58d3e723e766ba57a984ab65d"      # Apna API Hash yahan dalein
BOT_TOKEN = "8523789813:AAGN7UPz54iFcxfdmsHYGMbS3rpmhGEYT8k"    # Apna Bot Token yahan dalein
SUDO_USERS = [777756062]     # Apni Telegram ID yahan dalein
LOG_CHAT_ID = -1003481794992   # Log Group ID yahan dalein

bot = Client("final_search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Auth Filter
auth_filter = filters.create(lambda _, __, message: message.from_user and message.from_user.id in SUDO_USERS)

# --- START & MENU UI ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    menu_keyboard = ReplyKeyboardMarkup([
        [KeyboardButton("🔍 Search Details"), KeyboardButton("👤 My Profile")],
        [KeyboardButton("🛠 Help & Support")]
    ], resize_keyboard=True)

    welcome_text = (
        f"🌟 **Namaste {message.from_user.first_name}!**\n\n"
        "Welcome to the **Deep Search Intelligence Bot**.\n"
        "Aap niche diye gaye menu ka use karke search kar sakte hain."
    )
    await message.reply_text(welcome_text, reply_markup=menu_keyboard)

# Menu Button Handlers
@bot.on_message(filters.regex("🔍 Search Details"))
async def search_btn(client, message):
    await message.reply_text("🔎 Search ke liye `/search` command ka use karein.\n\n"
                             "📌 **Format:**\n"
                             "• Number: `/search 9876543210`\n"
                             "• Username: `/search @username`\n"
                             "• Telegram ID: `/search 123456789`", 
                             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔍 Click to Search", switch_inline_query_current_chat="/search ")]]))

# --- MAIN SEARCH LOGIC (With Animation & Multi-Type Search) ---
@bot.on_message(filters.command("search") & auth_filter)
async def search_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ **Format:** `/search [Mobile/@Username/ID]`")
    
    query = message.text.split(None, 1)[1]
    
    # Identify Search Type
    search_type = "Mobile Number"
    if query.startswith("@"):
        search_type = "Telegram Username"
    elif query.isdigit() and len(query) > 10:
        search_type = "Telegram ID"

    # Animation
    msg = await message.reply_text(f"📡 **Identifying: {search_type}...**")
    await asyncio.sleep(0.7)
    await msg.edit("🔎 **Scanning Global Database...** ⏳")
    await asyncio.sleep(0.7)
    await msg.edit("🔓 **Decrypting Secure Records...** 🗝")

    try:
        # Logging Activity
        await client.send_message(LOG_CHAT_ID, f"🕵️ **New Search**\n👤 **By:** {message.from_user.mention}\n📂 **Type:** `{search_type}`\n🔍 **Query:** `{query}`")

        # --- DATABASE API LOGIC ---
        # Note: Yahan aapki API call hogi jo search_type ke hisab se data degi
        # r = requests.get(f"YOUR_API_URL?q={query}&type={search_type}").json()
        
        # Testing Dummy Data (Old structure preserved)
        dummy_res = {
            "status": "found", 
            "count": 1, 
            "data": [{
                "name": f"Result for {query}", 
                "fname": "Database Record", 
                "id": "634731473361", 
                "address": "Prayagraj!UP", 
                "mobile": query if not query.startswith("@") else "N/A"
            }]
        }
        
        report = format_detailed_result(dummy_res)
        
        # Adding Timestamp to fix 400 MESSAGE_NOT_MODIFIED
        final_report = f"{report}\n\n⏱️ **Processed:** `{time.strftime('%H:%M:%S')}`"
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 New Search", switch_inline_query_current_chat="/search ")]
        ])
        
        await msg.edit(final_report, reply_markup=buttons, disable_web_page_preview=False)

    except Exception as e:
        await msg.edit(f"❌ **System Error:** `{str(e)}`")

if __name__ == "__main__":
    keep_alive() # Start Flask server for Render
    print("🚀 Bot is live and professional!")
    bot.run()
    
