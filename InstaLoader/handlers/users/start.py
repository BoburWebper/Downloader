import os
import django
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from asgiref.sync import sync_to_async
from aiogram.utils.exceptions import ChatNotFound

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django
django.setup()

# Import Django models and other components
from loader import dp, bot  # Assuming dp is your Dispatcher instance
from telesave.models import Users  # Replace with your models
from data.config import ADMINS
from data.db_query import create_or_get_user

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    try:
        # Call create_or_get_user asynchronously
        user = await create_or_get_user(
            telegram_id=user_id,
            firstname=first_name,
            lastname=last_name,
            telegram_username=username,
        )

        if user:
            await message.answer(f"Salom {message.from_user.full_name}!")
            await message.answer("""
                Salom Men Tele Save Bot

    ✅ Mening xususiyatlarim bilan tanishing:

    Instagramdan - Video yuklash

    TikTokdan - Video yuklash

    YouTubedan - Video va musiqalarni yuklash""")

            # Notify admins about the new user
            # await bot.send_message(ADMINS, f"New user registered: {first_name}, {last_name}, {username}")

    except ChatNotFound:
        await message.answer("Error: Chat not found. Please try again later or contact support.")
    except Exception as e:
        # Handle other exceptions gracefully
        await message.answer(f"Error occurred while processing command: {e}")

