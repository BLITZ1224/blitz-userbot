import asyncio
import os
import re
import google.generativeai as genai
from pyrogram import Client, filters, idle
from flask import Flask
from threading import Thread
from datetime import datetime

# --- RENDER PORT SETUP ---
web = Flask(__name__)
@web.route('/')
def home(): return "BLITZ AI Assistant is Running!"

def run_web():
    # Render port setup
    port = int(os.environ.get("PORT", 10000))
    web.run(host='0.0.0.0', port=port)

# --- AI CONFIGURATION ---
# Your Gemini API Key
GEMINI_KEY = "AlzaSyC_NcH3jpOFjv_8439xT_Gd0lkm9eLacfU" 
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BOT CONFIGURATION ---
API_ID = 32642557  
API_HASH = "2790877135ea0991a392fe6a0d285c27"
STRING_SESSION = "BQHyFf0AErKl8lfBlk9HNLMV0_TTGH92io0UBo6-bXclv3o1AJO4-wZbGArXYRBf3QJ0YAzvC9i0n31ChVH7m_FmKGmaZ8wBwhPGbUcrphFjT6YBp3P3bl5aqe_jz-UyQ3N4z4vCNiPxH_rNp8cb_5W_VaOlk93LwToZ6ZT0ASySlTnGAYvETgu_tsUq9M2hork3mq6ZnPieFL-mtWu2EYwC02iZwKhGre0UvsaBdPykR7uN4NljK15C3ByNa5OFDtCxDmcqlKGI0oTIdvzBe3aRdb175WrbbcRVr-V9fDrhImcWS_Se1GW_fbFDxCbS_N2HJytzfmb7bCE3Lgjgx2s9s6dKhQAAAAGQ1m1ZAA"

# Session issues fixed with in_memory=True
app = Client(
    "blitz_session", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=STRING_SESSION, 
    in_memory=True
)

# --- TRACKING ---
last_message_time = {}

# --- SPECIAL USERS ---
GF_USERNAME = "thwe014"
BEST_FRIEND = "Goozxak12"

def get_ai_response(text, sender_username):
    # Male Persona Setup
    persona = (
        "မင်းက 'တိုးဝေအောင်' (Blitz) ဆိုတဲ့ ယောကျ်ားလေးရဲ့ AI Assistant ပါ။ \n"
        "တိုးဝေအောင်က မနက် ၆ ကနေ ညနေ ၆:၄၅ ထိ ကုမ္မဏီအလုပ်လုပ်ပြီး၊ ည ၁၀ ထိ Streamer လုပ်ပါတယ်။ \n"
        "စည်းမျဉ်းများ: \n"
        "- မိန်းကလေးသံ 'ရှင့်'၊ 'ရှင်' လုံးဝ မသုံးရ။ \n"
        "- ယောကျ်ားလေး ပီပီသသ 'ဗျာ'၊ 'ခင်ဗျ' သို့မဟုတ် ပေါ့ပေါ့ပါးပါးပဲ ပြောပါ။ \n"
        "- မြန်မာစာမဟုတ်ရင် မြန်မာလို ဘာသာပြန်ပေးပါ။ \n"
    )
    
    if sender_username == GF_USERNAME:
        persona += "စာပို့သူက ကောင်မလေးပါ။ 'သဲလေး' လို့ခေါ်ပြီး ချိုချိုသာသာပြောပါ။ နောက်ဆုံးမှာ 'ကိုကို့ကိုယ်စား AI က ပြန်ပေးတာပါ' လို့ ထည့်ပြောပါ။"
    elif sender_username == BEST_FRIEND:
        persona += "စာပို့သူက အရင်းနှီးဆုံးသူငယ်ချင်း 'ယဖ' ပါ။ ရင်းနှီးပွင့်လင်းစွာ ဆဲချင်လည်းပြန်ဆဲပြီး ပြောပါ။"
    elif "blitz" in text.lower():
        persona += "စာပို့သူက Fan ဖြစ်လို့ ယဉ်ယဉ်ကျေးကျေး ပြန်ဖြေပါ။"
    else:
        persona += "ယဉ်ယဉ်ကျေးကျေး ပြန်ဖြေပါ။ ဆဲလာရင် လျစ်လျူရှုပါ။"

    prompt = f"{persona}\n\nUser: {text}"
    response = model.generate_content(prompt)
    return response.text

# --- SECURITY ---
def is_unsafe(text):
    links = re.findall(r'(https?://[^\s]+)', text)
    unsafe_patterns = [".exe", ".apk", "free-gift", "hack", "login"]
    for link in links:
        if any(pattern in link.lower() for pattern in unsafe_patterns):
            return True
    return False

# --- COMMANDS ---
@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_pong(_, message):
    # Check if bot is alive
    await message.edit("🚀 **BLITZ Bot is Active!**\n📶 Hosting: Render Cloud")

# --- MESSAGE HANDLER ---
@app.on_message(filters.private)
async def handle_message(client, message):
    if not message.text: return
    chat_id = message.chat.id

    # If I reply personally
    if message.from_user.is_self:
        last_message_time[chat_id] = datetime.now()
        return

    # Link Security
    if is_unsafe(message.text):
        await message.delete()
        await message.reply_text("⚠️ **Security Alert:** မသင်္ကာစရာ Link ဖြစ်လို့ ဖျက်လိုက်ပါပြီ။")
        return

    # 2-Minute Timer Logic
    arrival_time = datetime.now()
    last_message_time[chat_id] = arrival_time
    
    await asyncio.sleep(120) 

    # Check if AI should still reply
    if last_message_time.get(chat_id) == arrival_time:
        history = [m async for m in client.get_chat_history(chat_id, limit=1)]
        if history and history[0].from_user.is_self:
            return

        response = get_ai_response(message.text, message.from_user.username)
        await client.send_chat_action(chat_id, "typing")
        await asyncio.sleep(2)
        await message.reply_text(response)

async def main():
    Thread(target=run_web).start()
    await app.start()
    print("🛰️ BLITZ AI Bot starting on Render...")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
