from channels.generic.websocket import AsyncJsonWebsocketConsumer


class RestaurantConsumer(AsyncJsonWebsocketConsumer):
    """
    Live order/KDS/POS stream for a single restaurant.

    Only authenticated staff may connect, and a client may only subscribe to a
    restaurant it belongs to. Clients are receive-only: inbound frames are
    ignored so a connected client can never inject events to other screens.
    """

    async def connect(self):
        user = self.scope.get('user')
        if user is None or not user.is_authenticated:
            await self.close(code=4401)  # Unauthorized
            return

        self.restaurant_id = self.scope['url_route']['kwargs'].get('restaurant_id', 'default')

        # A user scoped to a restaurant may only watch that restaurant's stream.
        user_restaurant_id = getattr(user, 'restaurant_id', None)
        if user_restaurant_id is not None and str(user_restaurant_id) != str(self.restaurant_id):
            await self.close(code=4403)  # Forbidden
            return

        self.room_group_name = f"restaurant_{self.restaurant_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content):
        # Receive-only: clients cannot broadcast. Ignore all inbound messages.
        return

    async def broadcast_event(self, event):
        # Server-initiated push to the connected client.
        await self.send_json({
            'type': event['event_type'],
            'payload': event['payload'],
        })
