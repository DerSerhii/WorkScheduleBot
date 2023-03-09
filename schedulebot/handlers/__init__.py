from aiogram import Dispatcher

from .superuser import register_superuser
from .admin import register_admin
from .employee import register_employee
from .start import register_start


__all__ = ['setup']


def setup(dp: Dispatcher):
    register_superuser(dp)
    register_admin(dp)
    register_employee(dp)
    register_start(dp)
