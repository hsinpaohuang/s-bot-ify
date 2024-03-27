from typing import cast
from use_cases.base_use_case import BaseUseCase
from repositories.base_repository import BaseReadOnlyRepository
from entities.base_entity import BaseEntity
from entities.user import UserEntity
from dtos.track import SpotifyTracks

class GetSpotifyTracksOfPlaylistUseCase[T: BaseEntity](BaseUseCase):
    def __init__(self, repo: BaseReadOnlyRepository[T]):
        self._repo = repo

    async def execute(self, user: UserEntity, playlist_id: str, offset: int = 0):
        return cast(
            SpotifyTracks,
            await self._repo.list(
                user=user,
                playlist_id=playlist_id,
                offset=offset,
            ),
        ) \
            .as_tracks
