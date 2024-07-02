import os
from io import BytesIO

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
import instaloader
from asgiref.sync import sync_to_async
from django.core.files import File

from handlers.users.tiktok import handle_tiktok_video
from handlers.users.youtube import send_youtube_image
from keyboards.inline.add_group import get_inline_keyboard
from loader import bot, dp
from telesave.models import VideosRequest, Users

# Ensure directories exist
os.makedirs('instagram', exist_ok=True)
os.makedirs('youtube', exist_ok=True)
os.makedirs('tiktok', exist_ok=True)

keyboard = get_inline_keyboard()

# Initialize Instaloader
L = instaloader.Instaloader()


# Handler for handling Instagram post URLs
@dp.message_handler(content_types=ContentType.TEXT)
async def handle_url(message: types.Message, state: FSMContext):
    url = message.text
    if "instagram.com" in url:
        await handle_insta_post(message, url)
    elif "tiktok.com" in url:
        await handle_tiktok_video(message, url)
    elif 'youtube.com' in url or 'youtu.be' in url:
        await send_youtube_image(message, url)
        # await state.set_state(YoutubeState.send_image)
        # Implement YouTube content download handling
        pass
    else:
        await message.reply("Video linki topilmadi")


async def handle_insta_post(message, url):
    try:
        waiting_message = await bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")

        # Strip and normalize the URL
        url = url.strip()

        # Extract shortcode from URL
        shortcode = url.split('/')[-2]
        print(f"Extracted shortcode: {shortcode}")

        # Create a Post instance from the shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Download the post content to 'instagram' folder
        target_dir = 'instagram'
        L.download_post(post, target=target_dir)

        # Determine the type of content and send accordingly
        if post.is_video:
            # If it's a video, construct the video path with upload date timestamp
            timestamp = post.date_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC")
            video_path = os.path.join(os.getcwd(), f"{target_dir}/{timestamp}.mp4")
            if os.path.exists(video_path):
                # Open and send the video file
                with open(video_path, 'rb') as video_file:
                    await bot.send_video(chat_id=message.chat.id, video=video_file,
                                         caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
                    await bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)
                    print(f"Video {timestamp}.mp4 sent successfully.")
            else:
                print(f"Video file {video_path} not found.")
        elif post.typename == 'GraphImage':
            # If it's an image, construct the image path with upload date timestamp
            timestamp = post.date_utc.strftime("%Y-%m-%d_%H-%M-%S_UTC")
            image_path = os.path.join(os.getcwd(), f"{target_dir}/{timestamp}.jpg")
            if os.path.exists(image_path):
                # Open and send the image file
                with open(image_path, 'rb') as image_file:
                    await bot.send_photo(chat_id=message.chat.id, photo=image_file,
                                         caption="@insta_tik_tokSaverbot orqali yuklab olindi 📥")
                    await bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)
                    print(f"Image {timestamp}.jpg sent successfully.")
            else:
                print(f"Image file {image_path} not found.")
        else:
            # Handle other types of content (optional)
            print(f"Unsupported content type for {shortcode}")

        print(f"Post {shortcode} downloaded and sent successfully.")

    except instaloader.exceptions.InstaloaderException as e:
        print(f"An Instaloader error occurred: {e}")
        await message.reply(f"Yuklab olishda xatolik: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
        await message.reply(f"xatolik: {e}")

