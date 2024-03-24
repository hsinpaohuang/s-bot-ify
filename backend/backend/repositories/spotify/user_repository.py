from typing import overload
from repositories.base_repository import BaseReadOnlyRepository
from entities.user import UserEntity
from dtos.user import SpotifyUser
from utils.spotify import SpotifyAPI

class SpotifyUserRepository(BaseReadOnlyRepository[UserEntity]):
    @overload
    async def get(self, input_data: UserEntity) -> SpotifyUser: ...
    @overload
    async def get(self, input_data: str) -> SpotifyUser: ...

    async def get(self, input_data: UserEntity | str):
        if type(input_data) == str:
            spotify_api = SpotifyAPI(access_token=input_data)
        elif type(input_data) == UserEntity:
            spotify_api = SpotifyAPI(input_data)
        else:
            raise ValueError('Invalid input_data')

        return await spotify_api.get('/v1/me', SpotifyUser)

    async def list(self): ...

    async def create(self): ...

    async def delete(self): ...

    async def upsert(self): ...

    async def update(self): ...
