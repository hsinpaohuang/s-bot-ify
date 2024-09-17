from typing import cast
from use_cases.base_use_case import BaseUseCase
from entities.base_entity import BaseEntity
from entities.user import UserEntity
from repositories.base_repository import BaseReadOnlyRepository
from dtos.playlist import PlaylistChatOnly

class GetChatMessageOfPlaylistUseCase[T: BaseEntity](BaseUseCase):
    def __init__(self, repo: BaseReadOnlyRepository[T]):
        self._repo = repo

    async def execute(self, user: UserEntity, playlist_id: str, before: str | None = None) -> PlaylistChatOnly:
        playlist = await self._repo.get(playlist_id, { 'user_id': user.id, 'before': before })

        if not playlist:
            return PlaylistChatOnly(history = [])

        return cast(PlaylistChatOnly, playlist)
