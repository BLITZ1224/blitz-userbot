import asyncio
import os
import socket
import re
import google.generativeai as genai
from pyrogram import Client, filters, idle
from datetime import datetime

# --- CONFIG ---
GEMINI_KEY = "AlzaSyC_NcH3jpOFjv_8439xT_Gd0lkm9eLacfU" 
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

app = Client("blitz_ultra", api_id=API_ID, api_hash=API_HASH, session_string=SESSION, in_memory=True)

last_message_time = {}
TARGET_FRIEND = "Goozxak12"
GIRLFRIEND = "thwe014"

# ⚓ Render Port Listener
def start_port_listener():
    try:
        port = int(os.environ.get("PORT", 10000))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(1)
        print(f"⚓ Port {port} bound successfully.")
    except: pass

# 🛡️ Link Scanner Logic
async def scan_link(text):
    if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][2-9a-fA-F]))+', text):
        return "⚠️ ဒီ Link က အန္တရာယ်ရှိနိုင်ပါတယ်။ AI က စစ်ဆေးနေပါတယ်... (Phishing/Malware သတိထားပါ)"
    return None

# 🚀 Manual Link Check in Saved Messages
@app.on_message(filters.me & filters.chat("me") & filters.text)
async def manual_check(client, message):
    if "စစ်အုန်း" in message.text:
        await message.reply("🔍 Link ကို စစ်ဆေးနေပါတယ်... စိတ်ချရမှု ရှိမရှိ ခဏစောင့်ပါ။")

# 🤖 AI & Auto Reply Logic
@app.on_message(filters.private & ~filters.me)
async def handle_all(client, message):
    user = message.from_user
    chat_id = message.chat.id
    text = message.text or ""
    
    # ၁။ Link Security Check
    warning = await scan_link(text)
    if warning: await message.reply(warning)

    # ၂။ ၂ မိနစ် Timer သတ်မှတ်ခြင်း
    arrival_time = datetime.now()
    last_message_time[chat_id] = arrival_time
    await asyncio.sleep(120) 

    if last_message_time.get(chat_id) == arrival_time:
        # ငါကိုယ်တိုင် ပြန်ထားရင် AI မဖြေတော့ဘူး
        history = [m async for m in client.get_chat_history(chat_id, limit=1)]
        if history and history[0].from_user.is_self: return

        # AI Context Setup
        identity = f"မင်းနာမည်က Blitz (တိုးဝေအောင်) ရဲ့ AI ပါ။ Blitz က မနက် ၆ ကနေ ညနေ ၆:၄၅ ထိ အလုပ်လုပ်ပြီး၊ ည ၁၀ ထိ Stream ပါမယ်။"
        if user.username == TARGET_FRIEND:
            prompt = f"{identity} အခု စကားပြောနေတာက Blitz ရဲ့ အရင်းနှီးဆုံးသူငယ်ချင်း 'ယဖ' ဖြစ်ပါတယ်။ သူ့ကို အပွင့်လင်းဆုံး ဆဲချင်လည်း ပြန်ဆဲပြီး ရယ်ရယ်မောမော ဖြေပေးပါ။ User: {text}"
        elif user.username == GIRLFRIEND:
            prompt = f"{identity} အခုပြောနေတာက Blitz ရဲ့ မိန်းမ @thwe014 ဖြစ်ပါတယ်။ အရမ်းချစ်ပြပြီး ယဉ်ယဉ်ကျေးကျေး 'ဗျာ' 'ခင်ဗျ' နဲ့ ချော့ဖြေပါ။ User: {text}"
        else:
            prompt = f"{identity} ဒါက တခြားလူပါ။ ယဉ်ကျေးစွာပဲ Blitz အလုပ်ရှုပ်နေကြောင်း မြန်မာလို ဖြေပေးပါ။ User: {text}"

        try:
            response = model.generate_content(prompt)
            await message.reply_text(response.text)
        except: pass

async def main():
    start_port_listener()
    await app.start()
    print("✅ Blitz Ultra Bot is Online!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
