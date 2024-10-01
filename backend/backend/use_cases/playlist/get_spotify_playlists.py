from .. import BaseUseCase
from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from entities.user import UserEntity

class GetSpotifyPlaylistsUseCase(BaseUseCase):
    def __init__(self, repo: SpotifyPlaylistRepository):
        self._repo = repo

    async def execute(self, user: UserEntity, offset: int = 0):
        playlist = await self._repo.list(user=user, offset=offset)

        return playlist.to_playlist(str(user.spotify_id))
