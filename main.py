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

bot = Client("secure_search_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Authorization Filter
def is_auth(_, client, message: Message):
    return message.from_user.id in SUDO_USERS
auth_filter = filters.create(is_auth)

@bot.on_message(filters.command("start"))
async def start(client, message):
    if message.from_user.id not in SUDO_USERS:
        return await message.reply_text("🚫 **Access Denied!** Admin se contact karein.")
    await message.reply_text(f"👋 **Hii {message.from_user.first_name}!**\nSearch ke liye type karein: `/search 8601513360`")

@bot.on_message(filters.command("add") & auth_filter)
async def add_user(client, message):
    if len(message.command) < 2:
        return await message.reply_text("💡 `/add [User_ID]`")
    uid = int(message.command[1])
    if uid not in SUDO_USERS:
        SUDO_USERS.append(uid)
        await message.reply_text(f"✅ User `{uid}` added to SUDO.")

@bot.on_message(filters.command("broadcast") & auth_filter)
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("💡 Message ko reply karke `/broadcast` likhein.")
    count = 0
    for user in SUDO_USERS:
        try:
            await message.reply_to_message.copy(user)
            count += 1
        except: pass
    await message.reply_text(f"📢 Broadcast Done! `{count}` users notified.")

@bot.on_message(filters.command("search") & auth_filter)
async def search_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("⚠️ `/search [Mobile/Name/ID]`")
    
    query = message.text.split(None, 1)[1]
    msg = await message.reply_text("🔎 **Deep Searching...**")
    
    try:
        # 🔗 APNI REAL API CONNECT KAREIN:
        # response = requests.get(f"https://your-api.com/search?q={query}").json()
        
        # Test Data implementation (remove this part when using real API)
        from search_engine import format_detailed_result
        # Dummy data call for simulation
        dummy_data = {"status": "found", "count": 1, "data": [{"mobile": query, "name": "User Name", "fname": "Father Name", "address": "City!State!India", "id": "12345678", "email": "test@gmail.com"}]}
        
        final_report = format_detailed_result(dummy_data)
        await msg.edit(final_report, disable_web_page_preview=False)
    except Exception as e:
        await msg.edit(f"❌ Error: `{str(e)}`")

print("Bot is LIVE! 🚀")
bot.run()
