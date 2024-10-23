from typing import Any
from repositories.playlist import PlaylistRepository
from entities.playlist import PlaylistEntity

class SaveChatStateOfPlaylistUseCase:
    def __init__(self, playlist_repo: PlaylistRepository) -> None:
        self.playlist_repo = playlist_repo

    async def execute(
        self,
        playlist: PlaylistEntity,
        chat_state: dict[str, Any]
    ) -> None:
        await self.playlist_repo.set_chat_state(playlist, chat_state)
