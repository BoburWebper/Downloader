from aiogram.dispatcher.filters.state import StatesGroup, State


class YoutubeState(StatesGroup):
    send_image = State()
    send_video = State()