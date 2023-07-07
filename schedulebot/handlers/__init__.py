from aiogram import Dispatcher

from .superuser import register_superuser_handlers
from .membership import register_membership_handlers
# from .admin import register_admin
# from .employee import register_employee
from .debug import register_debug


__all__ = ['setup']


def setup(dp: Dispatcher):
    """
    Handlers registration setup.

    ATTENTION! The order of registration is important!

    :param dp: Current update dispatcher.
    :type dp: :obj:`aiogram.Dispatcher`
    :return:
    """
    register_superuser_handlers(dp)
    register_membership_handlers(dp)
    # register_admin(dp)
    # register_employee(dp)
    register_debug(dp)
