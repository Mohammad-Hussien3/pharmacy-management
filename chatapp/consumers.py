from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):


    @database_sync_to_async
    def getUser(self, id):
        from django.contrib.auth.models import User
        return User.objects.get(id=id)
    
    @database_sync_to_async
    def getChatRoom(self, name, user):
        from .models import ChatRoomMessages
        if  ChatRoomMessages.objects.filter(name=self.room_group_name).exists():
            room = ChatRoomMessages.objects.get(name=name)
        else:
            room = ChatRoomMessages.objects.create(name=name, participant=user)
            room.save()
            
        return room
    
    @database_sync_to_async
    def saveMessage(self, content, user):
        from .models import Messages
        message = Messages.objects.create(content=content, whoSend=user, chatRoom=self.room)
        message.save()

    @database_sync_to_async
    def getLastMessages(self):
        from .models import Messages
        return list(Messages.objects.filter(chatRoom=self.room).order_by('-time'))
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.senderId = int(self.scope['url_route']['kwargs']['senderId'])
        self.receiverId = int(self.scope['url_route']['kwargs']['receiverId'])
        self.room_group_name = f'chat_{self.room_name}_{min(self.senderId, self.receiverId)}_{max(self.senderId, self.receiverId)}'
        
        user = await self.getUser(self.receiverId)
        self.room = await self.getChatRoom(self.room_group_name, user)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

        lastMessages = await self.getLastMessages()
        for message in lastMessages:
            await self.send(text_data=json.dumps({
                'message': message.content,
                'id':message.id
            }))
            await asyncio.sleep(0.05)
    

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        user = await self.getUser(self.senderId)
        await self.saveMessage(message, user)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
            'id':self.senderId
        }))
