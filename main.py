import asyncio
import os
import google.generativeai as genai
from pyrogram import Client, filters, idle
from flask import Flask
from threading import Thread

# --- RENDER PORT SETUP ---
web = Flask(__name__)
@web.route('/')
def home(): return "BLITZ AI Bot is Live!"

def run_web():
    # Render က ပေးတဲ့ Port ကိုယူမယ်၊ မရှိရင် 10000 သုံးမယ်
    port = int(os.environ.get("PORT", 10000))
    web.run(host='0.0.0.0', port=port)

# --- AI CONFIGURATION ---
GEMINI_KEY = "AlzaSyC_NcH3jpOFjv_8439xT_Gd0lkm9eLacfU" # မင်းပေးတဲ့ Key
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BOT CONFIGURATION ---
API_ID = 32642557  
API_HASH = "2790877135ea0991a392fe6a0d285c27"
STRING_SESSION = "BQHyFf0AErKl8lfBlk9HNLMV0_TTGH92io0UBo6-bXclv3o1AJO4-wZbGArXYRBf3QJ0YAzvC9i0n31ChVH7m_FmKGmaZ8wBwhPGbUcrphFjT6YBp3P3bl5aqe_jz-UyQ3N4z4vCNiPxH_rNp8cb_5W_VaOlk93LwToZ6ZT0ASySlTnGAYvETgu_tsUq9M2hork3mq6ZnPieFL-mtWu2EYwC02iZwKhGre0UvsaBdPykR7uN4NljK15C3ByNa5OFDtCxDmcqlKGI0oTIdvzBe3aRdb175WrbbcRVr-V9fDrhImcWS_Se1GW_fbFDxCbS_N2HJytzfmb7bCE3Lgjgx2s9s6dKhQAAAAGQ1m1ZAA"

app = Client("blitz_session", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION, in_memory=True)

# --- AI CHAT LOGIC ---
@app.on_message(filters.private & ~filters.me)
async def ai_reply(client, message):
    try:
        # AI ကို Instruction ပေးခြင်း (မင်းအကြောင်းတွေ ဒီမှာ ထည့်သင်လို့ရတယ်)
        prompt = f"မင်းက BLITZ ရဲ့ AI Assistant ပါ။ လူလိုပဲ ပေါ့ပေါ့ပါးပါး မြန်မာလို ပြန်ဖြေပေးပါ။ တစ်ဖက်လူက ပြောတာက: {message.text}"
        response = model.generate_content(prompt)
        await message.reply_text(response.text)
    except Exception as e:
        print(f"AI Error: {e}")

@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_pong(_, message):
    await message.edit("🚀 **BLITZ AI Bot is Active!**\n📶 Port: Fixed & AI: Online")

async def start_bot():
    Thread(target=run_web).start() # Web Port နှိုးမယ်
    print("🛰️ BLITZ AI Bot starting on Render...")
    await app.start()
    await idle()

if __name__ == "__main__":
    asyncio.run(start_bot())
