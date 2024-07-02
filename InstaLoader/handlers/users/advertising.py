import logging
import os

from aiogram import types
from aiogram.types import InputFile
from asgiref.sync import sync_to_async
import django

from data.config import ADMINS
from loader import dp, bot

# Ensure the environment variable is set before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django
django.setup()

from telesave.models import Users, Advertisement


@dp.message_handler(commands=['reklama'])
async def advertising(message: types.Message):
    # Convert ADMINS list elements to integers
    admin_ids = [int(admin) for admin in ADMINS]

    # Only proceed if the message is from an admin
    if message.from_user.id in admin_ids:
        users = await sync_to_async(list)(Users.objects.all())
        for user in users:
            print(user.telegram_id)
        advertisements = await sync_to_async(list)(Advertisement.objects.all())

        for user in users:
            if user.telegram_id:
                for ad in advertisements:
                    try:
                        if ad.image:
                            await bot.send_photo(chat_id=user.telegram_id, photo=InputFile(ad.image.path),
                                                 caption=ad.text)
                        elif ad.video:
                            await bot.send_video(chat_id=user.telegram_id, video=InputFile(ad.video.path),
                                                 caption=ad.text)
                        else:
                            await bot.send_message(chat_id=user.telegram_id, text=ad.text)
                    except Exception as e:
                        logging.error(f"Error sending advertisement {ad.id} to user {user.telegram_id}: {e}")
