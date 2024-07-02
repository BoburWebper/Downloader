# data/db_query.py

from asgiref.sync import sync_to_async
from telesave.models import Users  # Import your Django model


@sync_to_async
def create_or_get_user(telegram_id, firstname, lastname, telegram_username):
    # Example: Create or get user logic
    user, created = Users.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'firstname': firstname,
            'lastname': lastname,
            'telegram_username': telegram_username,
        }
    )
    return user
