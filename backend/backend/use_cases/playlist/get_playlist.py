from use_cases.base_use_case import BaseUseCase
from entities.user import UserEntity
from entities.playlist import PlaylistEntity
from repositories.playlist_repository import PlaylistRepository

class GetPlaylistUseCase(BaseUseCase):
    def __init__(self, repo: PlaylistRepository):
        self._repo = repo

    async def execute(
        self,
        playlist_id: str,
        user: UserEntity,
    ) -> PlaylistEntity | None:
        return await self._repo.get(playlist_id, { 'user_id': user.id })
