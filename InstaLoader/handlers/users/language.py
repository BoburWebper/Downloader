from aiogram import types

from keyboards.inline.lang import lang
from loader import dp


@dp.message_handler(commands=['lang'])
async def language(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Tilni tanlang", reply_markup=lang)
