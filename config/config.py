import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

#  Dir for data
OUTPUT_DATA_DIR = 'data/prepared/'
RAW_DIR = 'data/raw/'