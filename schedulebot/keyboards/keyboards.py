from enum import Enum, unique

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from .kbmaker import InlineMarkup, DefaultMarkup


@unique
class Button(Enum):
    EMPLOYEE = 'Я майстер ✂️️'
    ADMIN = 'Я адміністратор 👩‍💼'
    REQUEST = 'Надіслати запит ↗️'
    CANSEL = 'Відміна ❌'
    STAFF = 'Персонал 👨‍👨‍👧‍👧'
    SCHEDULE = 'Розклад 🗓'


class StartMarkup:
    @staticmethod
    def start() -> InlineKeyboardMarkup:
        buttons = [dict(text=Button.EMPLOYEE.value,
                        callback_data='employee'),
                   dict(text=Button.ADMIN.value,
                        callback_data='admin')]
        schema = [2]
        return InlineMarkup(buttons, schema).create()

    @staticmethod
    def confirm() -> InlineKeyboardMarkup:
        buttons = [dict(text=Button.REQUEST.value,
                        callback_data='fdsfsd'),
                   dict(text=Button.CANSEL.value,
                        callback_data='sdfsdf')]
        schema = [2]
        return InlineMarkup(buttons, schema).create()


class SuperuserMarkup:
    @staticmethod
    def main() -> ReplyKeyboardMarkup:
        schema = [2]
        buttons = [dict(text=Button.STAFF.value), Button.SCHEDULE.value]
        return DefaultMarkup(buttons, schema).create()
