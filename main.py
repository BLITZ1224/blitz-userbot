import asyncio
from pyrogram import Client, filters, idle

# --- CONFIGURATION ---
API_ID = 32642557  
API_HASH = "2790877135ea0991a392fe6a0d285c27"
STRING_SESSION = "BQHyFf0AErKl8lfBlk9HNLMV0_TTGH92io0UBo6-bXclv3o1AJO4-wZbGArXYRBf3QJ0YAzvC9i0n31ChVH7m_FmKGmaZ8wBwhPGbUcrphFjT6YBp3P3bl5aqe_jz-UyQ3N4z4vCNiPxH_rNp8cb_5W_VaOlk93LwToZ6ZT0ASySlTnGAYvETgu_tsUq9M2hork3mq6ZnPieFL-mtWu2EYwC02iZwKhGre0UvsaBdPykR7uN4NljK15C3ByNa5OFDtCxDmcqlKGI0oTIdvzBe3aRdb175WrbbcRVr-V9fDrhImcWS_Se1GW_fbFDxCbS_N2HJytzfmb7bCE3Lgjgx2s9s6dKhQAAAAGQ1m1ZAA"

# Bot Client ကို တည်ဆောက်ခြင်း
app = Client(
    "blitz_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True  # Server ပေါ်မှာ session file ရှုပ်မနေအောင် memory ထဲမှာပဲ သိမ်းမယ်
)

# --- COMMANDS ---
@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_pong(_, message):
    await message.edit("🚀 **BLITZ Bot is Active!**\n📶 Hosting: Render Cloud")

@app.on_message(filters.command("help", prefixes=".") & filters.me)
async def help_cmd(_, message):
    help_text = (
        "**BLITZ Userbot Menu**\n\n"
        "`.ping` - Check bot status\n"
        "`.help` - Show this menu"
    )
    await message.edit(help_text)

# --- MAIN RUNNER ---
async def start_bot():
    print("🛰️ BLITZ Bot ကို Render ပေါ်မှာ စတင်နှိုးနေပါပြီ...")
    try:
        await app.start()
        print("✅ Success! Bot အောင်မြင်စွာ Login ဝင်ပြီးပါပြီ။")
        # Bot ကို အမြဲတမ်း ပွင့်နေစေဖို့ idle() ကို သုံးထားတယ်
        await idle()
    except Exception as e:
        print(f"❌ Error occurred: {e}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    # Python 3.12+ တွေမှာ ဖြစ်တတ်တဲ့ Event Loop ပြဿနာကို ရှင်းဖို့
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_bot())
    except RuntimeError:
        # Loop မရှိရင် အသစ်တစ်ခု ဆောက်ပြီး မောင်းမယ်
        asyncio.run(start_bot())
