from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Define inline keyboard markup
async def get_inline_keyboard():
    # Define a button that adds the bot to a group
    button_add_to_group = InlineKeyboardButton("Gruppaga qoshish",
                                               url=f"https://t.me/insta_tik_tokSaverbot?startgroup=1")

    # Create inline keyboard markup
    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_add_to_group)

    return keyboard
