import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class RestaurantConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.restaurant_id = self.scope['url_route']['kwargs'].get('restaurant_id', 'default')
        self.room_group_name = f"restaurant_{self.restaurant_id}"

        # Join restaurant room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave restaurant room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        # Broadcast message to room group
        event_type = content.get('type', 'message')
        payload = content.get('payload', {})

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_event',
                'event_type': event_type,
                'payload': payload,
            }
        )

    async def broadcast_event(self, event):
        # Send message to WebSocket client
        await self.send_json({
            'type': event['event_type'],
            'payload': event['payload']
        })
