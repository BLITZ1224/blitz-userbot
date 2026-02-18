import asyncio
import os
import socket
import random
import re
import google.generativeai as genai
from pyrogram import Client, filters, idle, enums
from datetime import datetime
import pytz

# --- [ AI Config ] ---
genai.configure(api_key="AlzaSyC_NcH3jpOFjv_8439xT_Gd0lkm9eLacfU")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- [ Bot Credentials ] ---
# မင်းပေးထားတဲ့ အချက်အလက်တွေနဲ့ Session String အသေထည့်ထားတယ်
app = Client(
    "blitz_twin",
    api_id=32642557,
    api_hash="2790877135ea0991a392fe6a0d285c27",
    session_string="BQHyFf0ApP8EWZmGjpLEVSDKU6EDuuBUbBNVjCLCT_jcQ3bBw2_3MY9T85ZJA45WhceGEu3zte3iB3dkLsMb4KweEB8twUHN7PuWUSZ8lPPMuYwemytCFg4sRRROPgJbBpsNuavYgTYgxW5Xq8GxxWkj3KfcgJhINV93r0bxkZ2B_x8WhRkB-wnKDyNOPrc-50asOfByxZ0YrOQsIa8Pxhu76ZmKoWeWjcBnH1Zvw4ZRZqLv7YrUN0XNo1nN4Chj6RGtsh2Bg7-ygC1ZwcEKZp41loCydG7wGQf_wFmhU1cR6Pp4mzSzZ760TpjizFpXjCeANzsCSJvkfdVO_IKnDjBOnbrwAAAAGQ1m1ZAA",
    in_memory=True
)

# --- [ Usernames အတိအကျ ] ---
TARGET_FRIEND = "Goozxak12" # ယဖ
GIRLFRIEND = "thwe014"      # Baby
last_message_time = {}

def start_port_listener():
    try:
        port = int(os.environ.get("PORT", 10000))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"⚓ Render Port {port} bound successfully.")
    except: pass

@app.on_message(filters.private & ~filters.me)
async def blitz_ai_handler(client, message):
    if not message.text: return
    
    chat_id = message.chat.id
    user = message.from_user
    text = message.text

    # Link Scanner
    if re.search(r'http[s]?://', text):
        await message.reply("⚠️ ဒီ Link က အန္တရာယ်ရှိနိုင်လို့ မနှိပ်သေးဘဲ ခဏစောင့်ပေးပါ။")

    # ၂ မိနစ် (၁၂၀ စက္ကန့်) စောင့်မယ်
    arrival_time = datetime.now()
    last_message_time[chat_id] = arrival_time
    await asyncio.sleep(120) 

    # ၂ မိနစ်အတွင်း ကိုယ်တိုင် စာမပြန်မှ AI က ဝင်ဖြေမယ်
    if last_message_time.get(chat_id) == arrival_time:
        history = [m async for m in client.get_chat_history(chat_id, limit=1)]
        if history and history[0].from_user.is_self: return

        await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
        await asyncio.sleep(random.uniform(3, 7))

        # အချိန်အလိုက် Status သတ်မှတ်ခြင်း
        tz = pytz.timezone('Asia/Rangoon')
        h = datetime.now(tz).hour
        if 6 <= h < 18: status = "ကုမ္ပဏီမှာ အလုပ်လုပ်နေတုန်း (အလုပ်အရမ်းရှုပ်နေတယ်)"
        elif 18 <= h < 22: status = "ဂိမ်း Stream နေတုန်း (MLBB/PUBG ဆော့နေတယ်)"
        else: status = "အိပ်ရာထဲမှာ အနားယူနေတုန်း"

        identity = f"မင်းက Blitz (တိုးဝေအောင်) ပါ။ ရန်ကုန်သား၊ မြဝတီမှာနေတယ်။ စရိုက်က ဟာသနှောတယ်၊ လိုရင်းပဲပြောတယ်။ အခြေအနေ: {status}"

        # Username အလိုက် Prompt ခွဲခြားခြင်း
        if user.username == TARGET_FRIEND:
            prompt = f"{identity} အခုပြောနေတာက မင်းသူငယ်ချင်း 'ယဖ' (@Goozxak12) ပါ။ သူ့ကို 'ငါ/မင်း' သုံးပြီး အရမ်းရင်းနှီးတဲ့ပုံစံနဲ့ ဖြေပါ။ သူဆဲရင် ပြန်ဆဲပါ။ User ပြောတာက: {text}"
        elif user.username == GIRLFRIEND:
            prompt = f"{identity} အခုပြောနေတာက မင်းမိန်းမ 'Baby' (@thwe014) ပါ။ သူ့ကို 'ကိုကို' လို့ သုံးပြီး 'Baby' လို့ ချစ်ချစ်ခင်ခင် ခေါ်ပါ။ User ပြောတာက: {text}"
        else:
            prompt = f"{identity} တခြားလူတွေကိုတော့ 'အစ်ကို' သုံးပြီး ယဉ်ကျေးစွာ လိုရင်းပဲ ဖြေပေးပါ။ User ပြောတာက: {text}"

        try:
            response = model.generate_content(prompt)
            await message.reply_text(response.text)
        except: pass

async def main():
    start_port_listener()
    print("🛰️ Connecting to Telegram...")
    await app.start()
    print("✅ BLITZ ULTRA DIGITAL TWIN IS ONLINE!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
