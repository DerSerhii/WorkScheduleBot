import logging
from enum import Enum, unique

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from .kbmaker import InlineMarkup, DefaultMarkup
from ..config import Role


@unique
class Button(Enum):
    EMPLOYEE = 'Я %s ✂️' % Role.EMPLOYEE.value
    ADMIN = 'Я %s 👩‍💼' % Role.ADMIN.value
    # CONFIRM_ROLE = '🆗  Підтверджую — %s'
    # REJECT_ROLE = '↩️  Назад — Я помилилась 😱️'
    GRANT_ACCESS = '✅ Надати доступ до записів 🗓'
    DENY_ACCESS = '⛔️ До чорного списку 🚷'
    STAFF = 'Персонал 👨‍👨‍👧‍👧'
    SCHEDULE = 'Розклад 🗓'
    INVITE = 'Запросити 🙋‍♀️'
    REMOVE = 'Видалити 🙅‍♀️'
    OKAY = '🆗 Все вірно'
    BACK = '↩️ Назад'


class StartMarkup:
    @staticmethod
    def start() -> InlineKeyboardMarkup:
        buttons = [dict(text=Button.EMPLOYEE.value,
                        callback_data=Role.EMPLOYEE.value),
                   dict(text=Button.ADMIN.value,
                        callback_data=Role.ADMIN.value)]
        schema = [1, 1]
        return InlineMarkup(buttons, schema).create()

    @staticmethod
    def confirm_role() -> InlineKeyboardMarkup:
        buttons = [dict(text=Button.OKAY.value,
                        callback_data='confirm_role'),
                   dict(text=Button.BACK.value,
                        callback_data='reject_role')]
        schema = [2]
        return InlineMarkup(buttons, schema).create()

    @staticmethod
    def confirm_user() -> InlineKeyboardMarkup:
        buttons = [dict(text=Button.GRANT_ACCESS.value,
                        callback_data='confirm_user'),
                   dict(text=Button.DENY_ACCESS.value,
                        callback_data='reject_user')]
        schema = [1, 1]
        return InlineMarkup(buttons, schema).create()

    @staticmethod
    def acknowledgment_name() -> InlineKeyboardMarkup:
        buttons = [dict(text=Button.OK.value,
                        callback_data='OK'),
                   dict(text=Button.BACK.value,
                        callback_data='Back')]
        schema = [1, 1]
        return InlineMarkup(buttons, schema).create()

    @staticmethod
    def contact() -> ReplyKeyboardMarkup:
        markup_request = ReplyKeyboardMarkup(resize_keyboard=True,
                                             one_time_keyboard=True).add(
            KeyboardButton('☎️ Відправити контакт для авторизації ↗️',
                           request_contact=True)
        )
        return markup_request


class SuperuserMarkup:
    @staticmethod
    def main() -> ReplyKeyboardMarkup:
        buttons = [dict(text=Button.STAFF.value), Button.SCHEDULE.value]
        schema = [2]
        return DefaultMarkup(buttons, schema).create()

    @staticmethod
    def invite(is_exist: bool) -> InlineKeyboardMarkup:
        buttons = [dict(text=Button.INVITE.value,
                        callback_data='invite')]
        schema = [1]
        if is_exist:
            buttons.extend([dict(text=Button.REMOVE.value,
                                 callback_data='remove')])
            schema.extend([1])
        return InlineMarkup(buttons, schema).create()
