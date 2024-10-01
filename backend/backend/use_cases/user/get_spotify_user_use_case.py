from dtos.user import SpotifyUser
from entities.user import UserEntity
from .. import BaseUseCase
from repositories.spotify.user_repository import SpotifyUserRepository

class GetSpotifyUserUseCase(BaseUseCase):
    def __init__(self, repo: SpotifyUserRepository):
        self._repo = repo

    async def execute(
        self,
        user: UserEntity | None = None,
        access_token: str | None = None,
    ) -> SpotifyUser:
        return await self._repo.get_user(user, access_token)
