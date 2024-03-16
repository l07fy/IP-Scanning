from channels.generic.websocket import AsyncWebsocketConsumer
from .tasks import get_info
import json

class IPInfoConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.group_name = self.channel_name.replace('!','')
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):

        ip_addresses = set(json.loads(text_data)['ips'].replace(' ', '').split(','))

        # Send IPs to tasks Async
        for ip_address in ip_addresses:
            get_info.delay(ip_address, self.group_name)

    async def sendinfo(self, event):
        # Gets result from tasks to send it
        result = event['task_result']

        await self.send(text_data=json.dumps(result))