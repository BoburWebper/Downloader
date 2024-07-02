from django.contrib import admin

# Register your models here.
from telesave.models import Users, VideosRequest, Advertisement, Chanel

admin.site.register(Users)
admin.site.register(VideosRequest)
admin.site.register(Advertisement)
admin.site.register(Chanel)
