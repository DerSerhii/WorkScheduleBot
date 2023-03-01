import os
from enum import Enum

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


class Handler(Enum):
    START = 'start'
    CLIENT = 'client'
    MODERATOR = 'moderator'
    SUPERUSER = 'superuser'
