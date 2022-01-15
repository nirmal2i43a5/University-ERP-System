import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification
class notificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'test_notification'
        self.room_group_name = 'test_notification_group'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status':'connected'}))


    # Receive message from WebSocket
    def receive(self, text_data):
        self.send(text_data=json.dumps(text_data))


    def send_notification(self,event):
        data=event.get('value')
        self.send(text_data=json.dumps({
            'payload':data
        }))


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
