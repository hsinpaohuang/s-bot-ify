from .. import BaseUseCase
from repositories.spotify.track_repository import SpotifyTrackRepository
from entities.user import UserEntity

class GetSpotifyTracksOfPlaylistUseCase(BaseUseCase):
    def __init__(self, repo: SpotifyTrackRepository):
        self._repo = repo

    async def execute(
        self,
        user: UserEntity,
        playlist_id: str,
        offset: int = 0,
    ):
        spotify_tracks = await self._repo.list(user, playlist_id, offset)

        return spotify_tracks.as_tracks
