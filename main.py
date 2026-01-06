import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from search_engine import format_detailed_result

# --- CONFIG ---
API_ID = 22447622  # Replace with yours
API_HASH = "543b62d58d3e723e766ba57a984ab65d" 
BOT_TOKEN = "8523789813:AAGN7UPz54iFcxfdmsHYGMbS3rpmhGEYT8k"
SUDO_USERS = [777756062] # Replace with your Telegram User ID
import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from search_engine import format_detailed_result

# --- CONFIG ---
API_ID = 22447622 
API_HASH = "543b62d58d3e723e766ba57a984ab65d"
BOT_TOKEN = "8523789813:AAGN7UPz54iFcxfdmsHYGMbS3rpmhGEYT8k"
SUDO_USERS = [777756062] # Apni TG ID yahan dalein
LOG_CHAT_ID = -1003481794992 # Log Group/Channel ID

bot = Client("deep_search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Authorization Filter
def is_auth(_, client, message: Message):
    return message.from_user.id in SUDO_USERS
auth_filter = filters.create(is_auth)

@bot.on_message(filters.command("start"))
async def start(client, message):
    if message.from_user.id not in SUDO_USERS:
        return await message.reply_text("🚫 Access Denied! Admin se permission lein.")
    await message.reply_text(f"👋 **Hii {message.from_user.first_name}!**\nSearch ke liye `/search [Mobile/@Username/ID]` bhejien.")

@bot.on_message(filters.command("add") & auth_filter)
async def add_user(client, message):
    if len(message.command) < 2: return
    uid = int(message.command[1])
    if uid not in SUDO_USERS:
        SUDO_USERS.append(uid)
        await message.reply_text(f"✅ User `{uid}` ko access de diya gaya.")

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
        return await message.reply_text("⚠️ `/search [Mobile/Username/ID]`")
    
    query = message.text.split(None, 1)[1]
    
    # Identify Search Type
    s_type = "mobile"
    if query.startswith("@"): s_type = "username"
    elif query.isdigit() and len(query) > 10: s_type = "tg_id"

    # LOGGING
    await client.send_message(LOG_CHAT_ID, f"🕵️ **New Search**\n👤 **By:** {message.from_user.first_name}\n🔍 **Query:** `{query}`\n📂 **Type:** `{s_type}`")

    msg = await message.reply_text(f"🔎 Searching database for {s_type}...")
    
    try:
        # API INTEGRATION (Apni link yahan dalein)
        # res = requests.get(f"https://your-db.com/api?q={query}&type={s_type}").json()
        
        # Default testing with Dummy Data
        dummy = {"status": "found", "count": 1, "data": [{"name": "Test User", "id": "634731473361", "address": "New Delhi!India", "mobile": "8601513360"}]}
        
        report = format_detailed_result(dummy)
        await msg.edit(report, disable_web_page_preview=False)
    except Exception as e:
        await msg.edit(f"❌ Error: {e}")

print("Bot is Running... 🚀")
bot.run()
