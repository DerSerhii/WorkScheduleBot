import logging

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message


class StartFilter(BoundFilter):
    async def check(self, message: Message):
        data = ctx_data.get()

        logging.info('4. FILTER')
        logging.info(f'{data=} Quantity: {len(data)}')
        logging.info('>>> to next "process message"...')

        return {'from_filter': 'This is data from filter'}
