import json
from channels.generic.websocket import AsyncWebsocketConsumer
from optparse import OptionParser
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print('accepted')

    async def disconnect(self, close_code):
    # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print('reacheddd')
        print(text_data)
        text_data_json = json.loads(text_data)
        print('reach')
        message = text_data_json['message']
        print(message + ' :receive')
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        print(message + ' :chat_message')
        # Send message to WebSocket
        print([func for func in dir(ChatConsumer) if callable(getattr(ChatConsumer, func))])
        await self.send(text_data=json.dumps({ 'message': message}))