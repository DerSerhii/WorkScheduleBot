import logging
import os
from pathlib import Path
from enum import Enum

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Settings Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SUPERUSER_ID = int(os.getenv('SUPERUSER_ID'))

# Settings Database
DATABASE = os.getenv('DATABASE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_CONNECT = {
    'database': DATABASE,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'host': DB_HOST
}

# Settings Logging
LOG_CONFIG = {
    'format': u'%(filename) -17s'
              u'[LINE:%(lineno)d]'
              u'\t#%(levelname) -10s'
              u'[%(asctime)s] \t%(message)s',
    'level': logging.INFO
}


class Role(Enum):
    SUPERUSER = 'superuser'
    ADMIN = 'admin'
    EMPLOYEE = 'employee'
