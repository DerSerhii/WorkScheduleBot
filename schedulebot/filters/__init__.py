from aiogram import Dispatcher

from .test_filter import TestFilter
from .role import SuperuserFilter, RoleFilter, FileSelectionMenuAccessFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(TestFilter)
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(SuperuserFilter)
    dp.filters_factory.bind(FileSelectionMenuAccessFilter)
