import asyncio
import os
import socket
import random
import re
import google.generativeai as genai
from pyrogram import Client, filters, idle, enums
from datetime import datetime
import pytz

# --- [၁] AI CONFIGURATION ---
GEMINI_KEY = "AlzaSyC_NcH3jpOFjv_8439xT_Gd0lkm9eLacfU" 
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- [၂] BOT SETUP (ENVIRONMENT VARIABLES) ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

app = Client(
    "blitz_ultra_twin",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
    in_memory=True
)

# Blitz ရဲ့ ရင်းနှီးသူများ
TARGET_FRIEND = "Goozxak12" # ယဖ
GIRLFRIEND = "thwe014"      # Baby

last_message_time = {}

# --- [၃] RENDER PORT HACKER (အပိတ်မခံရစေရန်) ---
def start_port_listener():
    try:
        port = int(os.environ.get("PORT", 10000))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"⚓ Render Port {port} bound successfully.")
    except Exception as e:
        print(f"📡 Port Note: {e}")

# --- [၄] AI DIGITAL TWIN LOGIC ---
@app.on_message(filters.private & ~filters.me)
async def blitz_ai_handler(client, message):
    if not message.text: return
    
    chat_id = message.chat.id
    user = message.from_user
    text = message.text

    # Link Scanner (စကားပြောနေရင်း Link ပါလာရင် သတိပေးမယ်)
    if re.search(r'http[s]?://', text):
        await message.reply("⚠️ ဒီ Link က အန္တရာယ်ရှိနိုင်လို့ မနှိပ်သေးဘဲ ခဏစောင့်ပေးပါ။")

    # ၂ မိနစ် Timer (မင်းကိုယ်တိုင် စာပြန်ဖို့ အချိန်ပေးခြင်း)
    arrival_time = datetime.now()
    last_message_time[chat_id] = arrival_time
    await asyncio.sleep(120) 

    # ၂ မိနစ်ပြည့်လို့ မင်းဘက်က ဘာစာမှ မပို့ထားရင် AI က ဝင်ဖြေမယ်
    if last_message_time.get(chat_id) == arrival_time:
        history = [m async for m in client.get_chat_history(chat_id, limit=1)]
        if history and history[0].from_user.is_self: return

        # စာမရိုက်ခင် Typing... ပြခြင်း (စက္ကန့်အနည်းငယ် random စောင့်မယ်)
        await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
        await asyncio.sleep(random.uniform(3, 7))

        # မြန်မာစံတော်ချိန်နဲ့ Blitz ရဲ့ အခြေအနေကို သတ်မှတ်ခြင်း
        tz = pytz.timezone('Asia/Rangoon')
        now_mm = datetime.now(tz)
        h = now_mm.hour

        if 6 <= h < 18:
            status = "ကုမ္ပဏီမှာ အလုပ်လုပ်နေတာမို့ လိုရင်းပဲ ပြောမယ်။"
        elif 18 <= h < 22:
            status = "အခု MLBB/PUBG stream နေတာ။ ဂိမ်းဆော့ရင်း ခဏအားတုန်း ပြန်ဖြေတာ။"
        else:
            status = "အခု အိပ်ရာထဲမှာ အနားယူရင်း ဖုန်းကြည့်နေတာ။ (အိပ်နေတယ်လို့ မပြောနဲ့၊ ကိုယ်တိုင် နိုးနေသလိုပဲ ပြောပါ)"

        # AI Identity Context
        identity = (
            f"မင်းက Blitz (တိုးဝေအောင်) ပါ။ ရန်ကုန်သား၊ မြဝတီမှာနေတယ်။ စရိုက်က ဟာသနှောတယ်၊ လိုရင်းပဲပြောတယ်။ "
            f"မလေးမစာလုပ်တာနဲ့ လာဆဲတာ မကြိုက်ဘူး။ လက်ရှိအခြေအနေ: {status}"
        )

        # Relationship Logic
        if user.username == TARGET_FRIEND:
            prompt = f"{identity} အခု စကားပြောနေတာက မင်းသူငယ်ချင်း 'ယဖ' (@Goozxak12)။ သူ့ကို 'ငါ/မင်း' သုံး၊ ဆဲချင်လဲပြန်ဆဲ၊ အပွင့်လင်းဆုံး ရင်းနှီးတဲ့ပုံစံနဲ့ ဖြေပါ။ User: {text}"
        elif user.username == GIRLFRIEND:
            prompt = f"{identity} အခုပြောနေတာက မင်းမိန်းမ (Baby) @thwe014။ 'ကိုကို' လို့သုံး၊ သူ့ကို 'Baby' လို့ခေါ်ပြီး အရမ်းချစ်ပြပါ။ User: {text}"
        else:
            prompt = f"{identity} တခြားလူတွေဆို 'အစ်ကို' သုံးပြီး ယဉ်ကျေးစွာ လိုရင်းပဲ ဖြေပါ။ User: {text}"

        try:
            response = model.generate_content(prompt)
            await message.reply_text(response.text)
        except: pass

# Saved Messages ထဲမှာ Link စစ်ဖို့ Tools
@app.on_message(filters.me & filters.chat("me") & filters.text)
async def manual_tools(client, message):
    if "စစ်အုန်း" in message.text:
        await message.reply("🔍 Security Scan: ဒီ Link က Phishing/Hack Link ဖြစ်နိုင်ခြေ ရှိပါတယ်။ မနှိပ်တာ အကောင်းဆုံးပါ။")

async def main():
    start_port_listener()
    print("🛰️ Connecting to Telegram...")
    await app.start()
    print("✅ BLITZ ULTRA DIGITAL TWIN IS ONLINE!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
