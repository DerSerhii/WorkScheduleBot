import os
from pathlib import Path


from dotenv import load_dotenv


load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SUPERUSER = os.getenv('SUPERUSER_ID')

BASE_DIR = Path(__file__).resolve().parent

