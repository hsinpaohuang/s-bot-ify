from repositories.base_repository import BaseRepository
from entities.user import UserEntity
from dtos.playlist import SpotifyPlaylists
from utils.spotify import SpotifyAPI

class SpotifyPlaylistRepository(BaseRepository[UserEntity]):
    async def list(self, user: UserEntity, offset: int = 0):
        return await SpotifyAPI(user).get(
            '/v1/me/playlists',
            SpotifyPlaylists,
            params={ 'offset': str(offset), 'limit': '20' },
        )

    async def get(self): ...

    async def create(self): ...

    async def create_empty(self): ...

    async def delete(self): ...

    async def upsert(self): ...

    async def update(self): ...
