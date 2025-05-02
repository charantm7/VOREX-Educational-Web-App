import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatBox, ChatBoxMembership, Room
from django.core.exceptions import ObjectDoesNotExist

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
            self.room_group_name = f'chat_{self.room_id}'
            
            # Check if room exists and user has access
            room = await self.get_room()
            if not room:
                await self.close()
                return

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        except Exception as e:
            print(f"Error in connect: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            print(f"Error in disconnect: {str(e)}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            user = self.scope['user']

            # Save message to database
            await self.save_message(user, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': user.username
                }
            )
        except Exception as e:
            print(f"Error in receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Failed to process message'
            }))

    async def chat_message(self, event):
        try:
            message = event['message']
            sender = event['sender']

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender
            }))
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")

    @database_sync_to_async
    def get_room(self):
        try:
            return Room.objects.get(id=self.room_id)
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, user, message):
        try:
            room = Room.objects.get(id=self.room_id)
            chat_box = ChatBox.objects.get(room=room)
            ChatBoxMembership.objects.create(
                message_by=user,
                chat_box=chat_box,
                content=message
            )
        except Exception as e:
            print(f"Error saving message: {str(e)}") 