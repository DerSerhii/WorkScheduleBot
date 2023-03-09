from aiogram import types, Dispatcher

import schedulebot.messages as msg
import schedulebot.handlers.keyboards as kb


async def admin_confirm(call: types.CallbackQuery):
    await call.answer(cache_time=20)
    name = call.message.chat.first_name
    await call.message.answer(
        msg.POST_START % (name, 'керівнику'),
        reply_markup=kb.mkp_confirm_admin
    )


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        admin_confirm,
        kb.cb_start.filter(role='admin')
    )
