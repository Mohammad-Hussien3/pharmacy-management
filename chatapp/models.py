from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ChatRoomMessages(models.Model):
    name = models.CharField(max_length=100)
    participant = models.OneToOneField(User, related_name='chatroom', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Messages(models.Model):
    content = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)
    whoSend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send')
    chatRoom = models.ForeignKey(ChatRoomMessages, on_delete=models.CASCADE, related_name='messages')

    class Meta:
        indexes = [
            models.Index(fields=['chatRoom', 'time']),
        ]