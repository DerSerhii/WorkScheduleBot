"""
The module contains bot settings.

This module uses the role variable from `message` module. Therefore, they must be defined.
"""

import logging
import os
from pathlib import Path
from enum import Enum

from dotenv import load_dotenv

from schedulebot import messages as bot_msg


# Loads environment variables from a file <.env>
# file in the root folder
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Telegram Settings
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
SUPERUSER_ID = int(os.getenv('SUPERUSER_ID'))


# Database Settings
DB_CONNECT_SET = {
    'database': os.getenv('DATABASE'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST')
}


# Bot Role Settings
class Role(Enum):
    SUPERUSER = bot_msg.SUPERUSER.lower()
    ADMIN = bot_msg.ADMIN.lower()
    EMPLOYEE = bot_msg.EMPLOYEE.lower()


# Logging Settings
LOG_CONFIG = {
    'format': u'%(filename) -17s'
              u'[LINE:%(lineno)d]'
              u'\t#%(levelname) -10s'
              u'[%(asctime)s] \t%(message)s',
    'level': logging.INFO
}
