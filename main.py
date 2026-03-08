import os
import asyncio
from pyrogram import Client, filters
from flask import Flask
from threading import Thread
from config import Config
import strings

# Render အတွက် Port Binding
app = Flask('')
@app.route('/')
def home(): return "BLITZ USERBOT IS ONLINE! 🔥"
def run(): app.run(host='0.0.0.0', port=8080)

bot = Client("blitz_bot", Config.API_ID, Config.API_HASH, session_string=Config.SESSION)

# --- ၁။ Auto-Reply (Keyword Logic) ---
@bot.on_message(filters.private & ~filters.me & ~filters.bot)
async def auto_reply(client, message):
    text = message.text if message.text else ""
    # Seen ပြပြီး Typing ပြမည့်အပိုင်း
    await client.read_chat_history(message.chat.id)
    await client.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(2)
    
    reply_text = strings.get_response(text)
    await message.reply_text(reply_text)

# --- ၂။ .id (ID စစ်ဆေးခြင်း) ---
@bot.on_message(filters.me & filters.command("id", prefixes=Config.PREFIX))
async def check_id(client, message):
    target_id = message.chat.id
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
    await message.edit_text(f"🆔 **ID:** `{target_id}`")

# --- ၃။ .block (User Block) ---
@bot.on_message(filters.me & filters.command("block", prefixes=Config.PREFIX))
async def block_user(client, message):
    target_id = message.chat.id
    await client.block_user(target_id)
    await message.edit_text(f"🚫 User `{target_id}` ကို Block လိုက်ပြီ သားကြီး!")

# --- ၄။ .song (YouTube Search Logic) ---
@bot.on_message(filters.me & filters.command("song", prefixes=Config.PREFIX))
async def song_tool(client, message):
    query = " ".join(message.command[1:])
    if not query: return await message.edit("သီချင်းနာမည် ရိုက်ဦးလေ သားကြီး!")
    await message.edit(f"🎶 '{query}' ကို ရှာနေတယ်...")
    # ဤနေရာတွင် yt-dlp logic များကို ဆက်လက်ဖြည့်စွက်နိုင်သည်

# --- ၅။ .tt (TikTok Link Processing) ---
@bot.on_message(filters.me & filters.command("tt", prefixes=Config.PREFIX))
async def tt_tool(client, message):
    if len(message.command) < 2: return await message.edit("Link ထည့်ဦးလေ!")
    link = message.command[1]
    await message.edit("⏳ TikTok ဗီဒီယိုကို Logo မပါဘဲ ဒေါင်းနေတယ်...")

# --- ၆။ .bc (Broadcaster) ---
@bot.on_message(filters.me & filters.command("bc", prefixes=Config.PREFIX))
async def broadcast(client, message):
    text = " ".join(message.command[1:])
    if not text: return await message.edit("ပို့မည့်စာသား ရိုက်ဦးလေ!")
    await message.edit("📢 Broadcaster စနစ် စတင်နေပါပြီ...")

if __name__ == "__main__":
    Thread(target=run).start()
    print("BLITZ USERBOT STARTING...")
    bot.run()