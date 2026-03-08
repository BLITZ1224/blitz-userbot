import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    SESSION = os.environ.get("SESSION_STRING", "")
    OWNER_ID = 6724939097
    PREFIX = "."