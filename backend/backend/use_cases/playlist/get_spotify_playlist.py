from dtos.playlist import SpotifyPlaylist
from .. import BaseUseCase
from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from entities.user import UserEntity

class GetSpotifyPlaylistUseCase(BaseUseCase):
    def __init__(self, repo: SpotifyPlaylistRepository):
        self._repo = repo

    async def execute(
        self,
        user: UserEntity,
        playlist_id: str,
    ):
        spotify_playlist = await self._repo.get(user, playlist_id, response_model=SpotifyPlaylist)

        return spotify_playlist
