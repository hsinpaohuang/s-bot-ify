from typing import cast
from entities.user import UserEntity
from repositories.base_repository import BaseWriteOnlyRepository
from dtos.spotify_token import SpotifyToken

class SpotifyTokenRepository(BaseWriteOnlyRepository[UserEntity]):
    async def update(self, user: UserEntity, new_tokens: SpotifyToken):
        return cast(UserEntity, await user.set({
            'oauth_accounts.0.access_token': new_tokens.access_token,
            'oauth_accounts.0.expires_at': new_tokens.expires_at,
            'oauth_accounts.0.refresh_token': new_tokens.refresh_token,
        }))

    async def get(self): ...

    async def list(self): ...

    async def create(self): ...

    async def create_empty(self): ...

    async def delete(self): ...

    async def upsert(self): ...

