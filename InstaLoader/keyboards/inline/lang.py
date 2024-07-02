from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbekcha", callback_data="uzb"),
            InlineKeyboardButton(text="English", callback_data="eng"),
            InlineKeyboardButton(text="Ruscha", callback_data="eng"),
        ],
    ],
    resize_keyboard=True,
)

lang_uzb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uzb"),
            InlineKeyboardButton(text="English", callback_data="eng"),
            InlineKeyboardButton(text="Ruscha", callback_data="eng"),
        ],
    ],
    resize_keyboard=True,
)

lang_rus = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbekcha", callback_data="uzb"),
            InlineKeyboardButton(text="English", callback_data="eng"),
            InlineKeyboardButton(text="🇷🇺 Ruscha", callback_data="eng"),
        ],
    ],
    resize_keyboard=True,
)

lang_eng = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbekcha", callback_data="uzb"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="eng"),
            InlineKeyboardButton(text="Ruscha", callback_data="eng"),
        ],
    ],
    resize_keyboard=True,
)
