from dtos.chat import NewMessage
from .. import BaseUseCase
from entities.playlist import PlaylistEntity
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

    async def execute(
        self,
        playlist: PlaylistEntity,
        message: NewMessage,
        is_bot: bool = False,
    ):
        chat = message.to_chat_history(is_bot)
        return await self._repo.add_message(playlist, chat)


