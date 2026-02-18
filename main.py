import os
import asyncio
from flask import Flask
from threading import Thread
import google.generativeai as genai
from pyrogram import Client, filters

# Render အတွက် Web Server အသေးလေး (အိပ်မပျော်အောင် လုပ်ဖို့)
web_app = Flask('')

@web_app.route('/')
def home():
    return "BLITZ UserBot is Alive!"

def run_web():
    web_app.run(host='0.0.0.0', port=10000)

# 🔑 မင်းရဲ့ သော့ချက်များ
API_ID = 32642557 
API_HASH = "2790877135ea0991a392fe6a0d285c27"
GEMINI_API_KEY = "AIzaSyC2uhHVtSzRfBHUrVAiDs0BHUKLFKDcgME"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Client("blitz_session", api_id=API_ID, api_hash=API_HASH)

SYSTEM_PROMPT = "မင်းက BLITZ ဖြစ်တယ်။ MLBB Chou Specialist တစ်ယောက်။ စာပြန်ရင် အေးဆေးနဲ့ လူကြီးဆန်ဆန်၊ ရင်းရင်းနှီးနှီး မြန်မာလိုပဲ ပြန်ပေးပါ။"

@app.on_message(filters.private & ~filters.me)
async def ai_auto_reply(client, message):
    if not message.text: return
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(f"{SYSTEM_PROMPT} \n\n User message: {message.text}")
        await client.send_chat_action(message.chat.id, "typing")
        await asyncio.sleep(1.5) 
        await message.reply(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

# Bot နဲ့ Web Server ကို ပြိုင်တူမောင်းမယ်
if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    print("⚡ BLITZ UserBot Starting...")
    app.run()
