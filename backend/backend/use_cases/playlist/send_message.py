from dtos.chat import NewMessage
from use_cases.base_use_case import BaseUseCase
from entities.playlist import PlaylistEntity
from repositories.playlist_repository import PlaylistRepository

class SendMessageUseCase(BaseUseCase):
    def __init__(self, repo: PlaylistRepository):
        self._repo = repo

    async def execute(self, playlist: PlaylistEntity, message: NewMessage):
        chat = message.to_chat_history(is_bot = False)
        await self._repo.add_message(playlist, chat)


