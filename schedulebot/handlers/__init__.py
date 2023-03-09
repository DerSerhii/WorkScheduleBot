from aiogram import Dispatcher

from .start import register_start
from .superuser import register_superuser
from .admin import register_admin
from .employee import register_employee


__all__ = ['setup']


def setup(dp: Dispatcher):
    register_start(dp)
    register_superuser(dp)
    register_admin(dp)
    register_employee(dp)
