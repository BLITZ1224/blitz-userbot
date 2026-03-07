# Moon-Userbot - telegram userbot
# Modified for Render Hosting (Auto-Keep-Alive) by BLITZ

import logging
import os
import platform
import sqlite3
import subprocess
import threading # Flask ကို Background မှာ run ဖို့

import requests
from flask import Flask # Render မအိပ်အောင် Web Port ဖွင့်ဖို့
from pyrogram import Client, errors, idle
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.raw.functions.account import DeleteAccount, GetAuthorizations

from utils import config
from utils.db import db
from utils.misc import gitrepo, userbot_version
from utils.module import ModuleManager
from utils.rentry import rentry_cleanup_job
from utils.scripts import restart

# --- Flask Server Logic (Render Keep-Alive) ---
web_app = Flask('')

@web_app.route('/')
def home():
    return "<b>BLITZ AI Bot is Active! 🔥</b><br>Streaming By BLITZ is Running 24/7."

def run_web_server():
    # Render က ပေးတဲ့ Port ကို သုံးမယ်၊ မရှိရင် 8080 ကို သုံးမယ်
    port = int(os.environ.get("PORT", 8080))
    try:
        web_app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logging.error(f"Flask Server Error: {e}")

# Web Server ကို Background Thread နဲ့ နှိုးထားမယ်
threading.Thread(target=run_web_server, daemon=True).start()
# ----------------------------------------------

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
if SCRIPT_PATH != os.getcwd():
    os.chdir(SCRIPT_PATH)

common_params = {
    "api_id": config.api_id,
    "api_hash": config.api_hash,
    "hide_password": True,
    "workdir": SCRIPT_PATH,
    "app_version": userbot_version,
    "device_model": f"Moon-Userbot @ {gitrepo.head.commit.hexsha[:7]}",
    "system_version": platform.version() + " " + platform.machine(),
    "sleep_threshold": 30,
    "test_mode": config.test_server,
    "parse_mode": ParseMode.HTML,
}

if config.STRINGSESSION:
    common_params["session_string"] = config.STRINGSESSION

app = Client("my_account", **common_params)

def load_missing_modules():
    all_modules = db.get("custom.modules", "allModules", [])
    if not all_modules:
        return

    custom_modules_path = f"{SCRIPT_PATH}/modules/custom_modules"
    os.makedirs(custom_modules_path, exist_ok=True)

    try:
        f = requests.get(
            f"https://raw.githubusercontent.com/The-MoonTg-project/custom_modules/{config.modules_repo_branch}/full.txt"
        ).text
    except Exception:
        logging.error("Failed to fetch custom modules list")
        return
        
    modules_dict = {
        line.split("/")[-1].split()[0]: line.strip() for line in f.splitlines()
    }

    for module_name in all_modules:
        module_path = f"{custom_modules_path}/{module_name}.py"
        if not os.path.exists(module_path) and module_name in modules_dict:
            url = f"https://raw.githubusercontent.com/The-MoonTg-project/custom_modules/{config.modules_repo_branch}/{modules_dict[module_name]}.py"
            resp = requests.get(url)
            if resp.ok:
                with open(module_path, "wb") as f:
                    f.write(resp.content)
                logging.info("Loaded missing module: %s", module_name)
            else:
                logging.warning("Failed to load module: %s", module_name)

async def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("moonlogs.txt"), logging.StreamHandler()],
        level=logging.INFO,
    )
    DeleteAccount.__new__ = None

    try:
        await app.start()
    except sqlite3.OperationalError as e:
        if str(e) == "database is locked" and os.name == "posix":
            logging.warning("Session file is locked. Trying to kill blocking process...")
            subprocess.run(["fuser", "-k", "my_account.session"], check=True)
            restart()
        raise
    except (errors.NotAcceptable, errors.Unauthorized) as e:
        logging.error("%s: %s\nMoving session file to my_account.session-old...", e.__class__.__name__, e)
        os.rename("./my_account.session", "./my_account.session-old")
        restart()

    load_missing_modules()
    module_manager = ModuleManager.get_instance()
    info = db.get("core.updater", "restart_info")

    if info:
        try:
            await app.edit_message_text(info["chat_id"], info["message_id"], "<b>Loading modules...</b>")
        except errors.RPCError:
            pass

    await module_manager.load_modules(app)

    if info:
        text = {
            "restart": "<b>Restart completed!</b>",
            "update": "<b>Update process completed!</b>",
        }[info["type"]]

        if module_manager.failed_modules > 0:
            failed_list = "\n".join([f"• <code>{m}</code>" for m in module_manager.failed_list])
            text += f"\n\n[E] <b>Failed to load {module_manager.failed_modules} module(s):</b>\n{failed_list}\n\n<i>Please check logs for more details.</i>"
        try:
            await app.edit_message_text(info["chat_id"], info["message_id"], text)
        except errors.RPCError:
            pass
        db.remove("core.updater", "restart_info")

    if db.get("core.sessionkiller", "enabled", False):
        db.set("core.sessionkiller", "auths_hashes", [auth.hash for auth in (await app.invoke(GetAuthorizations())).authorizations])

    logging.info("Moon-Userbot started!")
    app.loop.create_task(rentry_cleanup_job())
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())