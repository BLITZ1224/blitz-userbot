import os
import asyncio
import google.generativeai as genai
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

# 🔑 မင်းရဲ့ သော့ချက်များ
API_ID = 32642557  #
API_HASH = "2790877135ea0991a392fe6a0d285c27"  #
GEMINI_API_KEY = "AIzaSyC2uhHVtSzRfBHUrVAiDs0BHUKLFKDcgME" #

# AI Config (Flash Model သုံးထားလို့ ပိုမြန်မယ်)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# UserBot Client
app = Client("blitz_session", api_id=API_ID, api_hash=API_HASH)

# AI ရဲ့ စရိုက် (System Prompt)
SYSTEM_PROMPT = "မင်းက BLITZ ဖြစ်တယ်။ MLBB Chou Specialist တစ်ယောက်။ စာပြန်ရင် အေးဆေးနဲ့ လူကြီးဆန်ဆန်၊ ရင်းရင်းနှီးနှီး မြန်မာလိုပဲ ပြန်ပေးပါ။"

@app.on_message(filters.private & ~filters.me)
async def ai_auto_reply(client, message):
    if not message.text: return

    try:
        # AI ဆီက အဖြေတောင်းမယ်
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(f"{SYSTEM_PROMPT} \n\n User message: {message.text}")
        
        # Typing... Effect ပြမယ်
        await client.send_chat_action(message.chat.id, "typing")
        await asyncio.sleep(1.5) 
        
        await message.reply(response.text)
        print(f"✅ Replied to {message.from_user.first_name}")

    except Exception as e:
        print(f"❌ Error: {e}")

print("⚡ BLITZ UserBot စတင်နေပါပြီ... စာလာပို့ရင် အလိုအလျောက် ပြန်ပေးပါလိမ့်မယ်။")
app.run()
