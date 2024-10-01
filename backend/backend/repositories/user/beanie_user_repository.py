from typing import cast
from . import UserRepository
from entities.user import UserEntity
from dtos.spotify_token import SpotifyToken

class BeanieTokenRepository(UserRepository):
    async def update_token(self, user: UserEntity, new_tokens: SpotifyToken):
        return cast(UserEntity, await user.set({
            'oauth_accounts.0.access_token': new_tokens.access_token,
            'oauth_accounts.0.expires_at': new_tokens.expires_at,
        }))
