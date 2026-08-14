import json

from channels.generic.websocket import AsyncWebsocketConsumer

GROUP = "comments"


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        await self.channel_layer.group_add(GROUP, self.channel_name)
        await self.accept()

    async def disconnect(self, code: int) -> None:
        await self.channel_layer.group_discard(GROUP, self.channel_name)

    async def comment_created(self, event: dict) -> None:
        await self.send(text_data=json.dumps(event["comment"]))
