import os

import django
from environs import Env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize Django
django.setup()


from telesave.models import Chanel

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
# INSTAGRAM_USERNAME = env.str("INSTAGRAM_USERNAME")
# INSTAGRAM_PASSWORD = env.str("INSTAGRAM_PASSWORD")
CHANNELS = []
chanels = Chanel.objects.all()
for chanel in chanels:
    CHANNELS.append(chanel.username)
