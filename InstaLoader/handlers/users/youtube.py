import os
from io import BytesIO

import requests
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from pytube import YouTube

from keyboards.inline.add_group import get_inline_keyboard
from loader import bot, dp
from keyboards.inline.youtube_keyboard import youtube_keyboard

keyboard = get_inline_keyboard()


class SessionMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        user_data = await dp.storage.get_data(user=message.from_user.id)
        data['user_data'] = user_data


dp.middleware.setup(SessionMiddleware())


async def send_youtube_image(message: types.Message, url: str):
    try:
        # await message.reply("Fetching YouTube thumbnail...")
        waiting_message = await bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")
        # Create a YouTube object
        yt = YouTube(url)

        # Extract the video ID from the URL
        video_id = yt.video_id

        # Form the URL for the thumbnail image
        thumbnail_url = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'

        # Download the thumbnail image
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            thumbnail_image = BytesIO(response.content)
            await bot.send_photo(message.chat.id, thumbnail_image, reply_markup=youtube_keyboard)
            # Save the URL to the user's session data
            await dp.storage.set_data(user=message.from_user.id, data={'youtube_url': url})
            await bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)
        else:
            await message.reply("Xatolik yuz berdi")

    except Exception as e:
        print(f"Error fetching YouTube thumbnail: {e}")
        await message.reply(f"Xatolik yuz berdi: {e}")


@dp.callback_query_handler(lambda c: c.data in ["video", "audio"])
async def handle_youtube_callback(callback_query: types.CallbackQuery):
    try:
        user_data = await dp.storage.get_data(user=callback_query.from_user.id)
        url = user_data.get('youtube_url')

        if not url:
            await bot.send_message(callback_query.from_user.id, "Link orqali video topilmadi.")
            return

        # await bot.send_message(callback_query.from_user.id, "Downloading video from YouTube...")
        waiting_message = await bot.send_message(callback_query.from_user.id, "⏳ Yuklanmoqda...")

        yt = YouTube(url)

        # Get the highest resolution video stream
        video_stream = yt.streams.get_highest_resolution()

        # Download the video into the 'youtube' directory
        video_filename = os.path.join('youtube', 'Audio.mp4')
        video_stream.download(filename=video_filename)

        # Check if there's an audio stream available
        if yt.streams.filter(only_audio=True):
            audio_stream = yt.streams.get_audio_only()

            # Download the audio into the 'youtube' directory
            audio_filename = os.path.join('youtube', 'Audio.mp4')
            audio_stream.download(filename=audio_filename)

            # Send video or audio based on user's choice
            if callback_query.data == 'video':
                with open(video_filename, 'rb') as video_file:
                    await bot.send_video(callback_query.from_user.id, video_file,
                                         caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
            elif callback_query.data == 'audio':
                with open(audio_filename, 'rb') as audio_file:
                    await bot.send_audio(callback_query.from_user.id, audio_file,
                                         caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=waiting_message.message_id)

    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        await bot.send_message(callback_query.from_user.id, f"Xatolik yuz berdi: {e}")
