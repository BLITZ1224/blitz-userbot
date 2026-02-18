import asyncio
from pyrogram import Client, filters, idle
from flask import Flask
from threading import Thread

# --- FAKE PORT FOR RENDER ---
web = Flask('')

@web.route('/')
def home():
    return "BLITZ Bot is Running!"

def run():
    web.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION ---
API_ID = 32642557  
API_HASH = "2790877135ea0991a392fe6a0d285c27"
STRING_SESSION = "BQHyFf0AErKl8lfBlk9HNLMV0_TTGH92io0UBo6-bXclv3o1AJO4-wZbGArXYRBf3QJ0YAzvC9i0n31ChVH7m_FmKGmaZ8wBwhPGbUcrphFjT6YBp3P3bl5aqe_jz-UyQ3N4<...>" # မင်းရဲ့ string အပြည့်အစုံထည့်ပါ

app = Client("blitz_session", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION, in_memory=True)

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_pong(_, message):
    await message.edit("🚀 **BLITZ Bot is Active!**\n📶 Hosting: Render Cloud")

async def start_bot():
    keep_alive() # Fake Port ကို စတင်နှိုးတာ
    print("🛰️ BLITZ Bot with Web Port starting...")
    await app.start()
    await idle()

if __name__ == "__main__":
    asyncio.run(start_bot())
