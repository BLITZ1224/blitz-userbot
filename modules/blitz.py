import random
import asyncio
import datetime
from pyrogram import Client, filters
from modules.strings import (
    GREETINGS, DOING_NOW, GAMING, WORK, ANIME, TECH, 
    WEATHER, MOTIVATION, JOKES, FOOD, HEALTH, MONEY, 
    SLEEP, MUSIC, INTERNET, BYE_MESSAGES, BRO_REPLIES, STICKER_REPLIES
)

# Global Variables
IS_RUNNING = True 
USER_CHAT_COUNT = {}
LAST_REPLIES = {}
COOLDOWN_USERS = {} 

def is_sleeping_time():
    now = datetime.datetime.now()
    # ည ၁ နာရီ မှ မနက် ၇ နာရီအတွင်း (Burmese Time)
    return 1 <= now.hour < 7

# --- Control Commands (.on / .off) ---
@Client.on_message(filters.me & filters.command("off", prefixes="."))
async def stop_bot(client, message):
    global IS_RUNNING
    IS_RUNNING = False
    await message.edit_text("❌ **Blitz AI Mode:** OFF")

@Client.on_message(filters.me & filters.command("on", prefixes="."))
async def start_bot(client, message):
    global IS_RUNNING
    IS_RUNNING = True
    await message.edit_text("✅ **Blitz AI Mode:** ON")

# --- Main Logic Handler ---
@Client.on_message(filters.private & ~filters.me & ~filters.bot)
async def blitz_handler(client, message):
    global IS_RUNNING, USER_CHAT_COUNT, LAST_REPLIES, COOLDOWN_USERS
    user_id = message.from_user.id
    
    # ၁။ Logic စစ်ဆေးခြင်း
    if not IS_RUNNING or is_sleeping_time() or user_id in COOLDOWN_USERS:
        return

    # ၂။ တစ်ယောက်ကို အကြောင်း ၃၀ ကန့်သတ်ချက်
    count = USER_CHAT_COUNT.get(user_id, 0)
    if count >= 30:
        return

    try:
        # ၃။ လူနဲ့တူအောင် ၂၀ စက္ကန့် စောင့်မယ်
        await asyncio.sleep(20)
        
        # သားကြီး ကိုယ်တိုင် စာပြန်ထားရင် Bot က ဝင်မရှုပ်တော့ဘူး
        async for msg in client.get_chat_history(message.chat.id, limit=1):
            if msg.from_user and msg.from_user.is_self:
                return

        # ၄။ Seen ပြခြင်း နှင့် Typing... ပြခြင်း
        await client.read_chat_history(message.chat.id)
        await client.send_chat_action(message.chat.id, "typing")
        
        # ၅။ Content Type အလိုက် အဖြေရွေးခြင်း
        source = BRO_REPLIES # Default
        reply_type = "text"

        if message.sticker:
            if STICKER_REPLIES:
                source = STICKER_REPLIES
                reply_type = "sticker"
            else:
                source = ["စတစ်ကာလေး မိုက်တယ်ဗျာ!"]
        elif message.photo or message.video:
            source = ["ပုံလေး (သို့) ဗီဒီယိုလေး တွေ့တယ်နော်၊ ခဏနေမှ သေချာကြည့်ပြီး ပြန်လိုက်မယ်။"]
        else:
            text = message.text.lower() if message.text else ""
            
            # Keyword Matching for Category
            if any(k in text for k in ["hi", "hello", "ဟယ်လို", "နေကောင်း"]): source = GREETINGS
            elif any(k in text for k in ["ဘာလုပ်", "doing", "လုပ်နေ"]): source = DOING_NOW
            elif any(k in text for k in ["mlbb", "ဂိမ်း", "rank", "ဆော့"]): source = GAMING
            elif any(k in text for k in ["အလုပ်", "စာရင်း", "company", "accounting"]): source = WORK
            elif any(k in text for k in ["anime", "one piece", "luffy"]): source = ANIME
            elif any(k in text for k in ["code", "python", "script", "bot", "tech"]): source = TECH
            elif any(k in text for k in ["နေပူ", "မိုးရွာ", "ရာသီဥတု"]): source = WEATHER
            elif any(k in text for k in ["စိတ်ညစ်", "အားပေး", "ပင်ပန်း"]): source = MOTIVATION
            elif any(k in text for k in ["ဟာသ", "ရယ်ရ", "joke"]): source = JOKES
            elif any(k in text for k in ["စား", "ဗိုက်ဆာ", "မုန့်"]): source = FOOD
            elif any(k in text for k in ["နေမကောင်း", "ကျန်းမာရေး", "ဆေး"]): source = HEALTH
            elif any(k in text for k in ["ပိုက်ဆံ", "ဈေး", "money", "ဝယ်"]): source = MONEY
            elif any(k in text for k in ["အိပ်", "အိပ်ချင်", "night"]): source = SLEEP
            elif any(k in text for k in ["သီချင်း", "music", "နားထောင်"]): source = MUSIC
            elif any(k in text for k in ["လိုင်း", "internet", "wifi"]): source = INTERNET
            elif any(k in text for k in ["bye", "သွားပြီ", "နားတော့"]): source = BYE_MESSAGES
            elif any(k in text for k in ["သားကြီး", "bro", "ဟျောင့်", "အကို"]): source = BRO_REPLIES

        # အဖြေမထပ်အောင် ရွေးမယ်
        reply_content = random.choice(source)
        while len(source) > 1 and reply_content == LAST_REPLIES.get(user_id):
            reply_content = random.choice(source)

        # ၆။ စာရိုက်ချိန် ဟန်ဆောင်ခြင်း (၃ စက္ကန့် မှ ၈ စက္ကန့်)
        await asyncio.sleep(random.randint(3, 8))

        # ၇။ ပြန်စာပို့ခြင်း
        if reply_type == "sticker":
            await message.reply_sticker(reply_content)
        else:
            await message.reply_text(reply_content)
        
        LAST_REPLIES[user_id] = reply_content

        # ၈။ Stats Update & Cooldown (၃၀ စက္ကန့်)
        USER_CHAT_COUNT[user_id] = count + 1
        COOLDOWN_USERS[user_id] = True
        await asyncio.sleep(30) 
        if user_id in COOLDOWN_USERS:
            del COOLDOWN_USERS[user_id]

    except Exception as e:
        print(f"Blitz Logic Error: {e}")