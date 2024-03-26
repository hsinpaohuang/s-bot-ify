from typing import cast
from use_cases.base_use_case import BaseUseCase
from repositories.base_repository import BaseReadOnlyRepository
from entities.base_entity import BaseEntity
from entities.user import UserEntity
from dtos.playlist import SpotifyPlaylists

class GetSpotifyPlaylistsUseCase[T: BaseEntity](BaseUseCase):
    def __init__(self, repo: BaseReadOnlyRepository[T]):
        self._repo = repo

    async def execute(self, user: UserEntity, offset: int = 0):
        return cast(
            SpotifyPlaylists,
            await self._repo.list(user=user, offset=offset)) \
                .to_playlist(str(user.spotify_id),
        )
