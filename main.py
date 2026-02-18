import asyncio
import os
from pyrogram import Client, filters, idle
from flask import Flask
from threading import Thread

# --- RENDER WEB ALIVE ---
web = Flask(__name__)
@web.route('/')
def home(): return "BLITZ BOT IS ALIVE"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host='0.0.0.0', port=port)

# --- BOT SETUP (SIMPLE VERSION) ---
API_ID = 32642557  
API_HASH = "2790877135ea0991a392fe6a0d285c27"
# Environment Variable ထဲက SESSION ကိုပဲ သုံးမယ်
STRING_SESSION = os.environ.get("SESSION")

app = Client(
    "blitz_session", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=STRING_SESSION, 
    in_memory=True
)

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_pong(_, message):
    await message.edit("🚀 **BLITZ Bot is Active!**")

@app.on_message(filters.private & ~filters.me)
async def simple_reply(_, message):
    # အရင်ဆုံး အလုပ်ဖြစ်အောင် ရိုးရိုး reply လေးပဲ အရင်စမ်းမယ်
    if "hi" in message.text.lower():
        await message.reply_text("ဟေး... ခဏနေမှ ပြန်လာခဲ့မယ်!")

async def main():
    Thread(target=run_web).start()
    await app.start()
    print("✅ Telegram Connected!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
