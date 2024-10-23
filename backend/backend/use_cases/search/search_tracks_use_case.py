from typing import Literal
from repositories.spotify.track_repository import SpotifyTrackRepository
from entities.user import UserEntity

class SearchTracksUseCase:
    def __init__(self, track_repository: SpotifyTrackRepository):
        self.track_repository = track_repository

    async def execute(
        self,
        user: UserEntity,
        query: str,
        search_type: Literal['name', 'genre'],
        artist: str,
        page: int = 0,
    ):
        return await self.track_repository.search(
            user,
            query,
            search_type,
            artist,
            page,
        )
