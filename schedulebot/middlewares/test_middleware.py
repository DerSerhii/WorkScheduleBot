import logging

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update, Message

from ..config import SUPERUSER_ID


class TestMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: Update, data: dict):
        logging.info('!!! SENT A NEW UPDATE !!!')
        logging.info('1. PRE PROCESS UPDATE')
        data['middleware'] = 'I was created in first point "pre process update"'

        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
        else:
            raise CancelHandler()

        logging.info(f'{data=} Quantity: {len(data)}')
        logging.info('>>> to next "process update"...')

    async def on_process_update(self, update: Update, data: dict):
        logging.info('2. PROCESS UPDATE')
        logging.info(f'{data=} Quantity: {len(data)}')
        logging.info('>>> to next "pre process message"...')

    async def on_pre_process_message(self, message: Message, data: dict):
        logging.info('3. PRE PROCESS MESSAGE')
        logging.info(f'{data=} Quantity: {len(data)}')
        logging.info('>>> to next "filter"...')

    async def on_process_message(self, message: Message, data: dict):
        logging.info('5. PROCESS MESSAGE')
        logging.info(f'{data=} Quantity: {len(data)}')
        data['middleware'] = 'It will fall into "handler"'
        logging.info('>>> to next "handler"...')

    async def on_post_process_message(self, message: Message,
                                      data_from_handler: list,
                                      data: dict):
        logging.info('7. POST PROCESS MESSAGE')
        logging.info(f'{data=} {data_from_handler=} Quantity: {len(data)}')
        logging.info('>>> to next "post process update"...')

    async def on_post_process_update(self, message: Message,
                                      data_from_handler: list,
                                      data: dict):
        logging.info('8. POST PROCESS UPDATE')
        logging.info(f'{data=} {data_from_handler=} Quantity: {len(data)}')
        logging.info('!!! THE END UPDATE !!!')
