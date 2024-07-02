import os
import requests
from aiogram import types

from keyboards.inline.add_group import get_inline_keyboard
from loader import bot, dp  # Adjust this import based on your actual bot setup
from aiogram.types import ContentType

# Rapid API endpoint and headers
RAPID_API_URL = 'https://tiktok-video-no-watermark2.p.rapidapi.com/'
RAPID_API_KEY = '3e98ed8ce1msh1a05c8a7aede75ap1ccdb6jsn2f6f17651931'
HEADERS = {
    'Content-Type': 'application/json',
    'x-rapidapi-host': 'tiktok-video-no-watermark2.p.rapidapi.com',
    'x-rapidapi-key': RAPID_API_KEY
}

keyboard = get_inline_keyboard()


# Function to get TikTok video URL using Rapid API
def get_tiktok_video_url_rapid_api(url):
    try:
        response = requests.post(RAPID_API_URL, headers=HEADERS, json={"url": url}, timeout=30)
        response.raise_for_status()

        data = response.json()
        if 'data' in data and 'play' in data['data']:
            return data['data']['play']
        else:
            print(f"Unexpected response structure: {data}")
            return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code}, {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        return None
    except ValueError as e:
        print(f"Value error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# Telegram bot handler to handle TikTok video
async def handle_tiktok_video(message, url):
    try:
        waiting_message = await bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")

        # Get the TikTok video URL using Rapid API
        video_url = get_tiktok_video_url_rapid_api(url)

        if video_url:
            # Send the video directly by URL
            await message.reply_video(video_url, caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
            await bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

        else:
            await message.reply("Xatolik yuz berdi")
    except Exception as e:
        print(f"Error handling TikTok video: {e}")
        await message.reply(f"Xatolik: {e}")
