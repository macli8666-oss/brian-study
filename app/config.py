import os
from dotenv import load_dotenv

load_dotenv()

FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DATABASE_PATH = os.getenv("DATABASE_PATH", "brian_study.db")

FEISHU_BASE_URL = "https://open.larksuite.com/open-apis"
