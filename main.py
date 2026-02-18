import os
import asyncio
from flask import Flask
from threading import Thread
import google.generativeai as genai
from pyrogram import Client, filters

# 🌐 Render Web Server (၂၄ နာရီပတ်လုံး နိုးနေစေရန်)
web_app = Flask('')

@web_app.route('/')
def home():
    return "BLITZ UserBot is Online and Running!"

def run_web():
    # Render ရဲ့ Default Port 10000 ကို သုံးထားပါတယ်
    web_app.run(host='0.0.0.0', port=10000)

# 🔑 Render Environment Variables ထဲကနေ ဆွဲဖတ်ခြင်း
# အဲ့ဒီထဲမှာ နာမည်တွေ မှားမဖြည့်ဖို့ သတိပြုပါ
try:
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
except Exception as e:
    print(f"❌ Environment Variables Error: {e}")
    print("Render ရဲ့ Env Vars မှာ API_ID, API_HASH, GEMINI_API_KEY တို့ကို သေချာဖြည့်ခဲ့ပါ!")

# 🧠 Gemini AI Configuration (1.5 Flash Version)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 📱 UserBot Client Session
app = Client("blitz_session", api_id=API_ID, api_hash=API_HASH)

# 🎭 AI ရဲ့ စရိုက် (System Prompt)
SYSTEM_PROMPT = "မင်းက BLITZ ဖြစ်တယ်။ MLBB ဆော့တာဝါသနာပါတဲ့ Chou Specialist တစ်ယောက်။ စာပြန်ရင် အေးဆေးနဲ့ လူကြီးဆန်ဆန်၊ ရင်းရင်းနှီးနှီး မြန်မာလိုပဲ ပြန်ပေးပါ။"

@app.on_message(filters.private & ~filters.me)
async def ai_auto_reply(client, message):
    if not message.text:
        return

    try:
        # AI ဆီက အဖြေတောင်းယူခြင်း
        response = model.generate_content(f"{SYSTEM_PROMPT} \n\n User message: {message.text}")
        
        # Typing... ပုံစံပြပြီး ပိုပြီးလူနဲ့တူအောင် လုပ်ခြင်း
        await client.send_chat_action(message.chat.id, "typing")
        await asyncio.sleep(1.5) 
        
        # အဖြေပြန်ပို့ခြင်း
        await message.reply(response.text)
        print(f"✅ အကြောင်းပြန်ပြီးပါပြီ: {message.from_user.first_name}")

    except Exception as e:
        print(f"❌ AI Error: {e}")

# 🚀 Bot နဲ့ Web Server ကို တစ်ပြိုင်တည်း မောင်းနှင်ခြင်း
if __name__ == "__main__":
    # Web Server ကို Thread နဲ့ သီးသန့်မောင်းမယ်
    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    
    print("⚡ BLITZ UserBot စတင်နေပါပြီ... စာလာပို့ရင် အလိုအလျောက် ပြန်ပေးပါလိမ့်မယ်။")
    app.run()
