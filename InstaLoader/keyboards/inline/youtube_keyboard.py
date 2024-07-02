from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
youtube_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Video', callback_data='video'),
            InlineKeyboardButton(text='Audio', callback_data='audio')
        ],
    ],
    resize_keyboard=True
)
# youtube_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
# youtube_keyboard.add(types.KeyboardButton("Video"))
# youtube_keyboard.add(types.KeyboardButton("Audio"))
