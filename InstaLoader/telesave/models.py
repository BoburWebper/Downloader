from django.db import models


class Users(models.Model):
    telegram_id = models.TextField(primary_key=True, unique=True)
    firstname = models.CharField(max_length=40, null=True, blank=True)
    lastname = models.CharField(max_length=40, null=True, blank=True)
    telegram_username = models.CharField(max_length=40, unique=True, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True, default='uz')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.telegram_id}"


class VideosRequest(models.Model):
    user_tg_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_tg_id')
    url = models.URLField()
    video_file = models.FileField(upload_to='media/videos/', null=True, blank=True)
    music = models.FileField(upload_to='media/music/', null=True, blank=True)
    image = models.FileField(upload_to='media/image/', null=True, blank=True)
    request_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request {self.id} by user {self.user_tg_id.telegram_id}"


class Advertisement(models.Model):
    text = models.TextField(null=False)
    image = models.ImageField(upload_to='media/advertising/image', null=True, blank=True)
    video = models.FileField(upload_to='media/advertising/video', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.text


class Chanel(models.Model):
    username = models.TextField(null=False)

    def __str__(self):
        return self.username
