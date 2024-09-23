from django.contrib import admin
from .models import ChatRoomMessages, Messages
# Register your models here.

admin.site.register(ChatRoomMessages)
admin.site.register(Messages)
