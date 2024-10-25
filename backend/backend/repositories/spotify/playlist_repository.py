from typing import List
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

    async def add_tracks(self, user: UserEntity, playlist_id: str, track_uris: List[str]):
        await SpotifyAPI(user).post(
            f'/v1/playlists/{playlist_id}/tracks',
            None,
            data={ 'uris': track_uris },
        )
