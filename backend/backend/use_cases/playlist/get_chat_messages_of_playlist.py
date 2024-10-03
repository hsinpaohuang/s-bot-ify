from .. import BaseUseCase
from entities.user import UserEntity
from dtos.playlist import PlaylistChatOnly
from repositories.playlist import PlaylistRepository

class GetChatMessageOfPlaylistUseCase(BaseUseCase):
    def __init__(self, repo: PlaylistRepository):
        self._repo = repo

    async def execute(
        self,
        user: UserEntity,
        playlist_id: str,
        before: str | None = None,
    ) -> PlaylistChatOnly:
        messages = await self._repo.get_messages(playlist_id, user, before)

        return messages or PlaylistChatOnly(history=[])
