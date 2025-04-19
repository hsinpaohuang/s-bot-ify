from typing import List, Type
from pydantic import BaseModel
from entities.user import UserEntity
from dtos.playlist import SpotifyPlaylist, SpotifyPlaylists
from utils.spotify import SpotifyAPI, Fields

class SpotifyPlaylistRepository():
    async def list(self, user: UserEntity, offset: int = 0):
        return await SpotifyAPI(user).get(
            '/v1/me/playlists',
            SpotifyPlaylists,
            params={ 'offset': str(offset), 'limit': '20' },
        )

    async def get[T: BaseModel](self, user: UserEntity, playlist_id: str, response_model: Type[T] = SpotifyPlaylist):
        fields: Fields = { 'tracks': { 'total': True } }
        return await SpotifyAPI(user).get(
            f'/playlists/{playlist_id}',
            response_model,
            params={ 'fields': SpotifyAPI.convert_fields(fields) }
        )

    async def add_tracks(self, user: UserEntity, playlist_id: str, track_uris: List[str]):
        await SpotifyAPI(user).post(
            f'/v1/playlists/{playlist_id}/tracks',
            None,
            data={ 'uris': track_uris },
        )
