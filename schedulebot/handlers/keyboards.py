from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# START
cb_start = CallbackData('start', 'role')
mkp_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardMarkup(text='Я майстер ✂️️',
                              callback_data=cb_start.new(role='client'))],
        [InlineKeyboardMarkup(text='Я адміністратор 👩‍💼',
                              callback_data=cb_start.new(role='admin'))]
    ]
)

# CONFIRM ROLE
cb_confirm_admin = CallbackData('confirm_role', 'confirm')
mkp_confirm_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Надіслати запит ↗️',
                              callback_data=cb_confirm_admin.new(confirm='send')),
         InlineKeyboardButton(text='Відміна ❌',
                              callback_data=cb_confirm_admin.new(confirm='cancel'))]
    ]
)
