from dtos.chat import NewMessage
from .. import BaseUseCase
from entities.user import UserEntity
from repositories.playlist import PlaylistRepository
from use_cases.playlist.get_playlist import GetPlaylistUseCase

class SendMessageUseCase(BaseUseCase):
    def __init__(
        self,
        repo: PlaylistRepository,
        get_playlist_use_case: GetPlaylistUseCase,
    ):
        self._repo = repo
        self._get_playlist_use_case = get_playlist_use_case

    async def execute(self, playlist_id: str, user: UserEntity, message: NewMessage):
        playlist = await self._get_playlist_use_case.execute(playlist_id, user)
        chat = message.to_chat_history(is_bot = False)
        await self._repo.add_message(playlist, chat)


