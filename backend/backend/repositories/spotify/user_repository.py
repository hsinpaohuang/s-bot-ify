from entities.base_entity import BaseEntity
from repositories.base_repository import BaseReadOnlyRepository
from dtos.spotify_user import SpotifyUser
from utils.aiohttp_session import session
from utils.spotify import SPOTIFY_API_V1_URL, make_header

class SpotifyUserRepository(BaseReadOnlyRepository[BaseEntity]):
    async def get(self, token: str):

        headers = make_header(token)
        url = f'{SPOTIFY_API_V1_URL}/v1/me'

        async with session.get(url, headers=headers) as resp:
            resp_data = await resp.json()
            if not resp.ok:
                raise RuntimeError(resp_data['error'])

            return SpotifyUser(**resp_data)

    async def list(self): ...

    async def create(self): ...

    async def delete(self): ...

    async def upsert(self): ...
