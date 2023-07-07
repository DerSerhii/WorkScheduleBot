import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery


class TestFilter(BoundFilter):
    async def check(self, call: CallbackQuery):
        data = ctx_data.get()
        state = Dispatcher.get_current().current_state()
        state_data = await state.get_data()
        logging.info(f'{state_data=}')


        logging.info(f"{call.data=}")
        logging.info('4. FILTER')
        logging.info(f'{data=} Quantity: {len(data)}')
        logging.info('>>> to next "process message"...')

        return {'from_filter': 'This is data from filter'}
