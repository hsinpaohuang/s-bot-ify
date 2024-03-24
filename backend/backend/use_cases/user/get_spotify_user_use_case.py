from typing import cast, overload
from dtos.user import SpotifyUser
from entities.base_entity import BaseEntity
from use_cases.base_use_case import BaseUseCase
from repositories.base_repository import BaseReadOnlyRepository

class GetSpotifyUserUseCase[T: BaseEntity](BaseUseCase):
    repo: BaseReadOnlyRepository[T]

    def __init__(self, repo: BaseReadOnlyRepository[T]):
        self._repo = repo

    @overload
    async def execute(self, input: BaseEntity) -> SpotifyUser: ...
    @overload
    async def execute(self, input: str) -> SpotifyUser: ...

    async def execute(self, input: BaseEntity | str) -> SpotifyUser:
        return cast(SpotifyUser, await self._repo.get(input))
