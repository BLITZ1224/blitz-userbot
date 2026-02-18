import os
import asyncio
from flask import Flask
from threading import Thread
import google.generativeai as genai
from pyrogram import Client, filters

# 🌐 Render Web Server
web_app = Flask('')
@web_app.route('/')
def home(): return "BLITZ UserBot is Alive!"
def run_web(): web_app.run(host='0.0.0.0', port=10000)

# 🔑 Variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ✅ Async Loop Error ကို ကျော်ဖို့ 
async def main():
    app = Client("blitz_session", api_id=API_ID, api_hash=API_HASH)
    
    SYSTEM_PROMPT = "မင်းက BLITZ ဖြစ်တယ်။ MLBB Chou Specialist တစ်ယောက်။ စာပြန်ရင် အေးဆေးနဲ့ လူကြီးဆန်ဆန်၊ ရင်းရင်းနှီးနှီး မြန်မာလိုပဲ ပြန်ပေးပါ။"

    @app.on_message(filters.private & ~filters.me)
    async def ai_auto_reply(client, message):
        if not message.text: return
        try:
            response = model.generate_content(f"{SYSTEM_PROMPT} \n\n User message: {message.text}")
            await client.send_chat_action(message.chat.id, "typing")
            await asyncio.sleep(1.5) 
            await message.reply(response.text)
        except Exception as e: print(f"❌ Error: {e}")

    print("⚡ BLITZ UserBot Starting...")
    await app.start()
    print("✅ Bot is Online!")
    await asyncio.Event().wait() # Bot ကို အမြဲပွင့်နေစေဖို့

if __name__ == "__main__":
    # Web Server ကို နိုးထားမယ်
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    
    # Python 3.14 error ကို ဖြေရှင်းဖို့ loop သစ်ဆောက်မယ်
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
