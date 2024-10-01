from entities.user import UserEntity
from dtos.playlist import SpotifyPlaylists
from utils.spotify import SpotifyAPI

class SpotifyPlaylistRepository():
    async def list(self, user: UserEntity, offset: int = 0):
        return await SpotifyAPI(user).get(
            '/v1/me/playlists',
            SpotifyPlaylists,
            params={ 'offset': str(offset), 'limit': '20' },
        )
