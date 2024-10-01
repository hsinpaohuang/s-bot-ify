from .. import BaseUseCase
from repositories.user import UserRepository
from entities.user import UserEntity
from dtos.spotify_token import SpotifyToken

class UpdateAccessTokenUseCase(BaseUseCase):
    def __init__(self, user_repo: UserRepository):
        self._repo = user_repo

    async def execute(self, user: UserEntity, token: SpotifyToken):
        return await self._repo.update_token(user, token)
