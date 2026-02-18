import asyncio
from pyrogram import Client, filters

# မင်းရဲ့ အချက်အလက်တွေ
API_ID = 32642557  
API_HASH = "2790877135ea0991a392fe6a0d285c27"
STRING_SESSION = "BQHyFf0AErKl8lfBlk9HNLMV0_TTGH92io0UBo6-bXclv3o1AJO4-wZbGArXYRBf3QJ0YAzvC9i0n31ChVH7m_FmKGmaZ8wBwhPGbUcrphFjT6YBp3P3bl5aqe_jz-UyQ3N4z4vCNiPxH_rNp8cb_5W_VaOlk93LwToZ6ZT0ASySlTnGAYvETgu_tsUq9M2hork3mq6ZnPieFL-mtWu2EYwC02iZwKhGre0UvsaBdPykR7uN4NljK15C3ByNa5OFDtCxDmcqlKGI0oTIdvzBe3aRdb175WrbbcRVr-V9fDrhImcWS_Se1GW_fbFDxCbS_N2HJytzfmb7bCE3Lgjgx2s9s6dKhQAAAAGQ1m1ZAA"

# Bot ကို စတင်သတ်မှတ်ခြင်း
app = Client(
    "blitz_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# Bot အလုပ်လုပ်ကြောင်း စမ်းသပ်ရန် (.ping လို့ ရိုက်ကြည့်ပါ)
@app.on_message(filters.command("ping", prefixes=".") & filters.me)
async def ping_pong(_, message):
    await message.edit("🚀 **BLITZ Bot is Active!**\n📶 Connection: Perfect")

async def main():
    print("🛰️ Server ပေါ်မှာ BLITZ Bot ကို စတင်မောင်းနှင်နေပါပြီ...")
    await app.start()
    print("✅ Bot Is Online!")
    # Bot ကို အမြဲတမ်း ပွင့်နေစေဖို့ idle() ကို သုံးထားတယ်
    from pyrogram.methods.utilities.idle import idle
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
