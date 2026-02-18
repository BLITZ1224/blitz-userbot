import asyncio
import os
import socket
import re
import google.generativeai as genai
from pyrogram import Client, filters, idle
from threading import Thread
from datetime import datetime

# --- PORT HACKER (Render အငြိမ်ဖမ်းဖို့) ---
def port_hacker():
    port = int(os.environ.get("PORT", 10000))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(f"⚓ Port {port} bound successfully.")
    while True:
        try:
            client, addr = s.accept()
            client.send(b"HTTP/1.1 200 OK\n\nBLITZ ALIVE")
            client.close()
        except:
            pass

# --- AI CONFIGURATION ---
GEMINI_KEY = "AlzaSyC_NcH3jpOFjv_8439xT_Gd0lkm9eLacfU" 
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BOT SETUP ---
API_ID = 32642557  
API_HASH = "2790877135ea0991a392fe6a0d285c27"
STRING_SESSION = os.environ.get("SESSION")

app = Client(
    "blitz_session", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=STRING_SESSION, 
    in_memory=True
)

last_message_time = {}

# --- COMMANDS ---
@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_pong(_, message):
    await message.edit("🚀 **BLITZ Bot is Active!**\n📶 Mode: Port Hack")

# --- AI RESPONSE LOGIC (၂ မိနစ် Timer ပါပြီးသား) ---
@app.on_message(filters.private & ~filters.me)
async def handle_ai_reply(client, message):
    if not message.text: return
    chat_id = message.chat.id
    arrival_time = datetime.now()
    last_message_time[chat_id] = arrival_time
    
    await asyncio.sleep(120) # ၂ မိနစ်စောင့်မယ်

    if last_message_time.get(chat_id) == arrival_time:
        history = [m async for m in client.get_chat_history(chat_id, limit=1)]
        if history and history[0].from_user.is_self:
            return

        # AI Persona
        prompt = f"မင်းက ယောကျ်ားလေး AI Assistant ပါ။ ယဉ်ယဉ်ကျေးကျေးနဲ့ 'ဗျာ' 'ခင်ဗျ' သုံးပြီးဖြေပါ။ User က ပို့တာက: {message.text}"
        response = model.generate_content(prompt)
        await message.reply_text(response.text)

async def main():
    Thread(target=port_hacker, daemon=True).start()
    print("🛰️ Connecting to Telegram...")
    await app.start()
    print("✅ BLITZ Bot is Online!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
