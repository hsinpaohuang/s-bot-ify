from pydantic import BaseModel
from use_cases.base_use_case import BaseUseCase
from entities.base_entity import BaseEntity
from repositories.base_repository import BaseWriteOnlyRepository

class UpdateAccessTokenUseCase[E: BaseEntity, D: BaseModel](BaseUseCase):
    def __init__(self, user_repo: BaseWriteOnlyRepository[E]):
        self._repo = user_repo

    async def execute(self, user: E, tokens: D):
        return await self._repo.update(user, tokens)
