"""
The module represents custom keyboard menus.
"""

from enum import Enum, unique

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from .kbmaker import InlineMarkup, DefaultMarkup
from ..config import Role
from .. import messages as bot_msg


@unique
class ButtonText(Enum):
    CONFIRM = '🆗 Все вірно, підтверджую!'
    BACK = '↩️ Відмінити та повернутися назад'

    EMPLOYEE = 'Я %s ✂️' % Role.EMPLOYEE.value
    ADMIN = 'Я %s 👩‍💼' % Role.ADMIN.value
    CONTACT = '☎️ Відправити контакт для авторизації ↗️'
    ACCEPT = '✅ Надати доступ'
    ACCEPT_WITHOUT_FILE = ACCEPT + ' поки що без файлу'
    REJECT = '🚷️ Внести до чорного списку'
    FILENAME = '🗓 %s'

    STAFF = '%s %s' % (bot_msg.STAFF_BADGE, bot_msg.STAFF)
    INVITE = '🙋‍♀️ Запросити ще'
    UPDATE = '📝 Редагувати дані'
    CLOSE = '❌ Закрити меню'

    SCHEDULE = '🗓 Розклад'


class MembershipMenuMarkup:
    """
    This object represents a set of custom keyboard markups for membership handlers.

    Each method implements a themed menu.
    """
    BTN_ACCEPT_WITHOUT_FILE = dict(text=ButtonText.ACCEPT_WITHOUT_FILE.value,
                                   callback_data='accepted')
    BTN_REJECT = dict(text=ButtonText.REJECT.value, callback_data='rejected')

    @classmethod
    def confirmation(cls, param='') -> InlineKeyboardMarkup:
        """
        CONFIRMATION MENU

        The inline keyboard markup consists of callback buttons:
            * [ CONFIRM ] — generates callback_data='confirmed:{param}',
            * [  BACK   ] — generates callback_data='back'.

        :param param: Serializable in JSON
        :return: :obj:`aiogram.types.InlineKeyboardMarkup`
        """
        btn_confirm = dict(text=ButtonText.CONFIRM.value, callback_data=f"confirmed:{param}")
        btn_back = dict(text=ButtonText.BACK.value, callback_data='back')

        buttons = [btn_confirm, btn_back]
        schema = [1, 1]
        return InlineMarkup(buttons, schema).create()

    @staticmethod
    def member_role_selection() -> InlineKeyboardMarkup:
        """
        MEMBER ROLE SELECTION MENU

        The inline keyboard markup consists of callback buttons:
            * [ EMPLOYEE ] — generates callback_data=Role.EMPLOYEE.value,
            * [  ADMIN   ] — generates callback_data=Role.ADMIN.value.

        :return: :obj:`aiogram.types.InlineKeyboardMarkup`.
        """
        buttons = [dict(text=ButtonText.EMPLOYEE.value, callback_data=Role.EMPLOYEE.value),
                   dict(text=ButtonText.ADMIN.value, callback_data=Role.ADMIN.value)]
        schema = [1, 1]
        return InlineMarkup(buttons, schema).create()

    @classmethod
    def applicant_consideration(cls, is_files: bool = True) -> InlineKeyboardMarkup:
        """
        APPLICANT CONSIDERATION MENU

        The inline keyboard markup consists of callback buttons:
            * [ ACCEPT ] — generates callback_data='accepted',
            * [ REJECT ] — generates callback_data='rejected'.

        :param is_files: Defaults to false, in which case the text ACCEPT button
            will be replaced with ACCEPT_WITHOUT_FILE.
        :type is_files: :obj:`base.Boolean`
        :return: :obj:`aiogram.types.InlineKeyboardMarkup`.
        """
        btn_accept = cls.BTN_ACCEPT_WITHOUT_FILE.copy()
        if is_files:
            btn_accept['text'] = ButtonText.ACCEPT.value
        buttons = [btn_accept, cls.BTN_REJECT]
        schema = [1, 1]
        return InlineMarkup(buttons, schema).create()

    @classmethod
    def member_file_selection(cls, files: list[dict]) -> InlineKeyboardMarkup:
        """
        MEMBER FILE SELECTION MENU

        The inline keyboard markup consists of callback buttons:
            * [     FILENAME 1      ] — generates callback_data='some_google_file_id',
            * [     FILENAME n      ] — n is an amount passed files,
            * [ ACCEPT_WITHOUT_FILE ] — generates callback_data='accepted',
            * [        REJECT       ] — generates callback_data='rejected'.

        :param files: List of dicts containing data about Document files.
        :type files: :obj:`base.List[base.Dict]`.
        :return: :obj:`aiogram.types.InlineKeyboardMarkup`.
        """
        buttons = []
        for file in files:
            if not ('id' in file and 'name' in file):
                raise ValueError(
                    "Incoming Document file data must contain keys: 'id' and 'name'")
            buttons.append(dict(text=ButtonText.FILENAME.value % file['name'],
                                callback_data=file['id']))
        buttons.extend([cls.BTN_ACCEPT_WITHOUT_FILE, cls.BTN_REJECT])
        schema = [1 for _ in files] + [1, 1]
        return InlineMarkup(buttons, schema).create()

    @staticmethod
    def send_contact() -> ReplyKeyboardMarkup:
        """
        CONTACT MENU
        
        The reply keyboard markup consists of the reply button at the bottom of the screen:
            * [ CONTACT ] — sends the applicant's contact (phone number).
        
        :return: :obj:`aiogram.types.ReplyKeyboardMarkup`.
        """
        btn_contact = KeyboardButton(ButtonText.CONTACT.value, request_contact=True)
        return ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True).add(btn_contact)


class ManagerMenuMarkup:
    """
    This object represents a set of custom keyboard markups for manager handlers.

    Each method implements a themed menu.
    """
    @staticmethod
    def main() -> ReplyKeyboardMarkup:
        """
        MAIN MANAGER MENU

        It is a main menu for manager handlers.

        The reply keyboard markup consists of reply buttons at the bottom of the screen:
            * [ STAFF ]   [ SCHEDULE ]

        :return: :obj:`aiogram.types.ReplyKeyboardMarkup`.
        """
        buttons = [dict(text=ButtonText.STAFF.value), ButtonText.SCHEDULE.value]
        schema = [2]
        return DefaultMarkup(buttons, schema).create()

    @staticmethod
    def staff() -> InlineKeyboardMarkup:
        """
        STAFF MENU

        The inline keyboard markup consists of callback buttons:
            * [ INVITE ] — generates callback_data='invite',
            * [ UPDATE ] — generates callback_data='update'.
            * [ REMOVE ] — generates callback_data='remove'.
            * [ CLOSE  ] — generates callback_data='close'.

        :return: :obj:`aiogram.types.InlineKeyboardMarkup`.
        """
        invite_btn = dict(text=ButtonText.INVITE.value, callback_data='invite')
        update_btn = dict(text=ButtonText.UPDATE.value, callback_data='update')
        remove_btn = dict(text=ButtonText.REJECT.value, callback_data='remove')
        close_btn = dict(text=ButtonText.CLOSE.value, callback_data='close')

        buttons = [invite_btn, update_btn, remove_btn, close_btn]
        schema = [1, 1, 1, 1]
        return InlineMarkup(buttons, schema).create()
