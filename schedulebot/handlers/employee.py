from aiogram import types, Dispatcher

import schedulebot.messages as msg


# async def client_confirm(call: types.CallbackQuery):
#     await call.answer(cache_time=20)
#     name = call.message.chat.first_name
#     await call.message.answer(
#         msg.CONFIRM_ROLE % (name, 'адміністратору'),
#         reply_markup=kb.mkp_confirm_admin
#     )
#
#
# def register_employee(dp: Dispatcher):
#     dp.register_callback_query_handler(
#         client_confirm,
#         kb.cb_start.filter(role='employee')
#     )
