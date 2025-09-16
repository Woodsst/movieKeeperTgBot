from aiogram import BaseMiddleware, types
from aiogram.dispatcher.event.bases import CancelHandler


class AccessMiddleware(BaseMiddleware):
    def __init__(self, allowed_ids: list[int]):
        super().__init__()
        self.allowed_ids = allowed_ids

    async def __call__(self, handler, event: types.Message, data):
        if event.from_user.id not in self.allowed_ids:
            raise CancelHandler()
        return await handler(event, data)
