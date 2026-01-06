import os, requests
from pyrogram import Client, filters
from security import is_admin

API = "http://YOUR_SERVER/search/mobile/"
HEAD = {"x-api-key": os.getenv("API_KEY")}

app = Client(
    "trackerbot",
    api_id=int(os.getenv("22447622")),
    api_hash=os.getenv("543b62d58d3e723e766ba57a984ab65d"),
    bot_token=os.getenv("8523789813:AAGN7UPz54iFcxfdmsHYGMbS3rpmhGEYT8k")
)

@app.on_message(filters.command("mobile"))
async def mobile_search(client, message):
    if not is_admin(message.from_user.id):
        return await message.reply("❌ Unauthorized")

    if len(message.command) < 2:
        return await message.reply("Use: /mobile 8601513360")

    num = message.command[1]
    res = requests.get(API + num, headers=HEAD).json()
    await message.reply(f"<pre>{res}</pre>")

app.run()
