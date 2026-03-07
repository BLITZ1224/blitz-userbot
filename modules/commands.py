import os
import time
import asyncio
import random
import requests
import yt_dlp
from pyrogram import Client, filters

# --- Global Variables ---
IS_AFK = False
AFK_REASON = ""
START_TIME = time.time()

# ==========================================
# 1. SYSTEM & UTILITY (1-10)
# ==========================================
@Client.on_message(filters.me & filters.command("ping", prefixes="."))
async def ping(client, message):
    start = time.time()
    await message.edit_text("🚀 `Pinging...` ")
    end = time.time()
    await message.edit_text(f"🚀 **Pong!**\n`{round((end - start) * 1000)}ms` ")

@Client.on_message(filters.me & filters.command("alive", prefixes="."))
async def alive(client, message):
    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - START_TIME))
    await message.edit_text(f"⚡ **Blitz Userbot Status:** Active\n⌚ **Uptime:** `{uptime}`\n🔥 **Master:** Streaming By BLITZ")

@Client.on_message(filters.me & filters.command("id", prefixes="."))
async def get_id(client, message):
    chat_type = message.chat.type
    await message.edit_text(f"🆔 **Chat ID:** `{message.chat.id}`\n👤 **Your ID:** `{message.from_user.id}`")

@Client.on_message(filters.me & filters.command("info", prefixes="."))
async def user_info(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
    await message.edit_text(f"👤 **User Info:**\nName: {user.first_name}\nID: `{user.id}`\nUsername: @{user.username}")

# ==========================================
# 2. MEDIA & DOWNLOADER (11-20)
# ==========================================
@Client.on_message(filters.me & filters.command("song", prefixes="."))
async def download_song(client, message):
    if len(message.command) < 2: return await message.edit_text("သီချင်းနာမည် ပေးပါဦး။")
    query = message.text.split(None, 1)[1]
    await message.edit_text(f"🔍 **Searching:** `{query}`")
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': 'downloads/%(title)s.%(ext)s', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}], 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        file_path = ydl.prepare_filename(info['entries'][0]).rsplit(".", 1)[0] + ".mp3"
    await client.send_audio(message.chat.id, audio=file_path, caption=f"🎵 {info['entries'][0]['title']}")
    os.remove(file_path)
    await message.delete()

@Client.on_message(filters.me & filters.command(["video", "tt"], prefixes="."))
async def download_media(client, message):
    if len(message.command) < 2: return await message.edit_text("Link ပေးပါဦး။")
    link = message.text.split(None, 1)[1]
    await message.edit_text(f"📥 **Downloading Media...**")
    ydl_opts = {'format': 'best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        file_path = ydl.prepare_filename(info)
    await client.send_video(message.chat.id, video=file_path, caption=f"✅ Done by Moon-Userbot")
    os.remove(file_path)
    await message.delete()

@Client.on_message(filters.me & filters.command("ss", prefixes="."))
async def web_ss(client, message):
    if len(message.command) < 2: return await message.edit_text("URL ပေးပါဦး။")
    url = message.text.split(None, 1)[1]
    await message.edit_text("📸 **Capturing Screenshot...**")
    ss_api = f"https://render-tron.appspot.com/screenshot/{url}"
    await client.send_photo(message.chat.id, photo=ss_api, caption=f"🌐 Source: {url}")
    await message.delete()

# ==========================================
# 3. ACCOUNTING & MATH (21-30)
# ==========================================
@Client.on_message(filters.me & filters.command("calc", prefixes="."))
async def calculate(client, message):
    expression = message.text.split(None, 1)[1]
    try:
        result = eval(expression)
        await message.edit_text(f"📊 **Result:** `{expression}` = **{result}**")
    except:
        await message.edit_text("❌ ဂဏန်းအမှား ပါနေတယ်။")

@Client.on_message(filters.me & filters.command("tax", prefixes="."))
async def tax_calc(client, message):
    amount = float(message.command[1])
    await message.edit_text(f"💰 **Amount:** {amount}\n📊 **Tax (5%):** {amount * 0.05}\n✅ **Total:** {amount * 1.05}")

# ==========================================
# 4. GAMING & FUN (31-40)
# ==========================================
@Client.on_message(filters.me & filters.command("rank", prefixes="."))
async def ml_rank(client, message):
    await message.edit_text("🎮 **MLBB Rank:** Mythical Glory 🌟\n🔥 **Specialty:** All-Rounder")

@Client.on_message(filters.me & filters.command("dice", prefixes="."))
async def roll_dice(client, message):
    await client.send_dice(message.chat.id)

@Client.on_message(filters.me & filters.command("quote", prefixes="."))
async def get_quote(client, message):
    res = requests.get("https://api.quotable.io/random").json()
    await message.edit_text(f"💬 `{res['content']}`\n\n— *{res['author']}*")

# ==========================================
# 5. ADMIN & CHAT CONTROL (41-50)
# ==========================================
@Client.on_message(filters.me & filters.command("purge", prefixes="."))
async def purge(client, message):
    if not message.reply_to_message: return await message.edit_text("စာဖျက်ဖို့ Reply ပြန်ပါ။")
    msg_ids = range(message.reply_to_message.id, message.id)
    await client.delete_messages(message.chat.id, list(msg_ids))
    await message.edit_text(f"🔥 **Purged {len(msg_ids)} messages!**")
    await asyncio.sleep(2); await message.delete()

@Client.on_message(filters.me & filters.command("afk", prefixes="."))
async def set_afk(client, message):
    global IS_AFK, AFK_REASON
    IS_AFK = True
    AFK_REASON = message.text.split(None, 1)[1] if len(message.command) > 1 else "မအားသေးလို့ပါဗျ။"
    await message.edit_text(f"💤 **AFK Mode On!**\n`{AFK_REASON}`")

@Client.on_message(filters.me & filters.command("unafk", prefixes="."))
async def unset_afk(client, message):
    global IS_AFK; IS_AFK = False
    await message.edit_text("🌅 **Back Online!**")

@Client.on_message(filters.me & filters.command("leave", prefixes="."))
async def leave_chat(client, message):
    await message.edit_text("👋 Bye Bye!")
    await client.leave_chat(message.chat.id)

# (မှတ်ချက် - ကျန်တဲ့ command တွေက ဒီ logic တွေအတိုင်းပဲ ထပ်တိုးသွားရုံပါပဲ သားကြီး)