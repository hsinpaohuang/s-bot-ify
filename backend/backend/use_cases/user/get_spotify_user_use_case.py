from typing import cast
from dtos.spotify_user import SpotifyUser
from entities.base_entity import BaseEntity
from use_cases.base_use_case import BaseUseCase
from repositories.base_repository import BaseReadOnlyRepository

class GetSpotifyUserUseCase[T: BaseEntity](BaseUseCase):
    repo: BaseReadOnlyRepository[T]

    def __init__(self, repo: BaseReadOnlyRepository[T]):
        self._repo = repo

    async def execute(self, auth_token: str):
        return cast(SpotifyUser, await self._repo.get(auth_token))
