from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DeliveryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the delivery ID from the URL
        self.delivery_id = self.scope['url_route']['kwargs']['delivery_id']
        await self.accept()
        await self.send(text_data=json.dumps({
            "message": f"Connected to delivery {self.delivery_id}!"
        }))

    async def receive(self, text_data=None, bytes_data=None):
        # Example: echo back
        await self.send(text_data=json.dumps({
            "echo": text_data,
            "delivery_id": self.delivery_id
        }))
