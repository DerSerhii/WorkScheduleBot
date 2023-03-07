from aiogram import Dispatcher

from .test_filter import TestFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(TestFilter)
