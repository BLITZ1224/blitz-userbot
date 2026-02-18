import asyncio
import os
import re
import google.generativeai as genai
from pyrogram import Client, filters, idle
from flask import Flask
from threading import Thread

# --- RENDER PORT SETUP ---
web = Flask(__name__)
@web.route('/')
def home(): return "BLITZ AI Assistant is Live!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web.run(host='0.0.0.0', port=port)

# --- AI CONFIGURATION ---
GEMINI_KEY = "AlzaSyC_NcH3jpOFjv_8439xT_Gd0lkm9eLacfU" #
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BOT CONFIGURATION ---
API_ID = 32642557  
API_HASH = "2790877135ea0991a392fe6a0d285c27"
STRING_SESSION = "BQHyFf0AErKl8lfBlk9HNLMV0_TTGH92io0UBo6-bXclv3o1AJO4-wZbGArXYRBf3QJ0YAzvC9i0n31ChVH7m_FmKGmaZ8wBwhPGbUcrphFjT6YBp3P3bl5aqe_jz-UyQ3N4z4vCNiPxH_rNp8cb_5W_VaOlk93LwToZ6ZT0ASySlTnGAYvETgu_tsUq9M2hork3mq6ZnPieFL-mtWu2EYwC02iZwKhGre0UvsaBdPykR7uN4NljK15C3ByNa5OFDtCxDmcqlKGI0oTIdvzBe3aRdb175WrbbcRVr-V9fDrhImcWS_Se1GW_fbFDxCbS_N2HJytzfmb7bCE3Lgjgx2s9s6dKhQAAAAGQ1m1ZAA"

app = Client("blitz_session", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION, in_memory=True)

# --- SPECIAL USERS ---
GF_USERNAME = "thwe014"
BEST_FRIEND = "Goozxak12"

# --- AI BRAIN (INSTRUCTIONS) ---
def get_ai_response(text, sender_username, is_me=False):
    persona = (
        "မင်းနာမည်က တိုးဝေအောင် (Blitz) ရဲ့ AI Assistant ပါ။ "
        "တိုးဝေအောင်က မနက် ၆ ကနေ ညနေ ၆:၄၅ အထိ ကုမ္မဏီအလုပ်လုပ်ပါတယ်။ ည ၁၀ နာရီအထိ Streamer လုပ်ပါတယ်။ "
        f"အခု စာပို့တဲ့သူက @{sender_username} ပါ။ "
    )
    
    if sender_username == GF_USERNAME:
        persona += "သူက တိုးဝေအောင်ရဲ့ ကောင်မလေးပါ။ အချိုသာဆုံးပြန်ပြောပါ။ နောက်ဆုံးမှာ 'ဒါက ကိုကို့ကိုယ်စား AI က ပြန်ပေးနေတာပါနော်' လို့ ထည့်ပြောပါ။"
    elif sender_username == BEST_FRIEND:
        persona += "သူက အရင်းနှီးဆုံးသူငယ်ချင်း 'ယဖ' ပါ။ ကြိုက်သလို ရင်းနှီးပွင့်လင်းစွာ ပြောပါ။ ဆဲရင်လည်း ပြန်ဆဲလို့ရပါတယ်။"
    elif "blitz" in text.lower():
        persona += "သူက Fan တစ်ယောက်ပါ။ ယဉ်ယဉ်ကျေးကျေးနဲ့ Streamer တစ်ယောက်လို ပြန်ဖြေပေးပါ။"
    else:
        persona += "ယဉ်ယဉ်ကျေးကျေး ပြန်ဖြေပါ။ ဆဲလာရင်တော့ လျစ်လျူရှုပါ။ မြန်မာစာမဟုတ်ရင် မြန်မာလို ဘာသာပြန်ပေးပါ။"

    prompt = f"{persona}\n\nUser text: {text}"
    response = model.generate_content(prompt)
    return response.text

# --- SECURITY: LINK CHECKER ---
def is_unsafe(text):
    # Link ပါမပါ စစ်မယ်
    links = re.findall(r'(https?://[^\s]+)', text)
    # ဥပမာ- .exe သို့မဟုတ် မသင်္ကာစရာ စာလုံးများ
    unsafe_patterns = [".exe", ".apk", "free-gift", "login-account", "hack"]
    for link in links:
        if any(pattern in link.lower() for pattern in unsafe_patterns):
            return True
    return False

# --- MESSAGE HANDLER ---
@app.on_message(filters.private)
async def handle_message(client, message):
    if not message.text: return

    # Link Security Check
    if is_unsafe(message.text):
        await message.delete()
        await message.reply_text("⚠️ **Security Alert:** မသင်္ကာစရာ Link ဖြစ်လို့ ဖျက်လိုက်ပါပြီ။")
        return

    # Saved Messages (For link scanning)
    if message.chat.id == (await client.get_me()).id:
        if "စစ်အုန်း" in message.text:
            await message.reply_text("🔍 Link ကို စစ်ဆေးနေပါတယ်... အန္တရာယ်မရှိတာ တွေ့ရပါတယ်။ (AI Analysis Demo)")
        return

    # AI Auto Reply (Not for me)
    if not message.from_user.is_self:
        # ၂ မိနစ် delay logic ကို ဒီမှာ ထည့်မထားသေးဘူး (အရင်ဆုံး AI အလုပ်လုပ်အောင် စမ်းမယ်)
        response = get_ai_response(message.text, message.from_user.username)
        await asyncio.sleep(2) # လူလိုဖြစ်အောင် ခဏစောင့်ပြီးမှ ပို့မယ်
        await message.reply_text(response)

async def main():
    Thread(target=run_web).start()
    await app.start()
    print("✅ BLITZ AI Assistant is Online & Live!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
