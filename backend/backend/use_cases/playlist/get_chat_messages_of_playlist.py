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
        playlist = await self._repo.get(playlist_id, user, before)

        if not playlist:
            return PlaylistChatOnly(history = [])

        return await self._repo.get_messages(playlist, before)
