from typing import Optional, Iterable
from abc import ABC, abstractmethod
from entities.base_entity import BaseEntity

# reference: https://fueled.com/the-cache/posts/backend/clean-architecture-with-fastapi/
# TODO: use default generic in python 3.13

class BaseReadOnlyRepository[T: BaseEntity](ABC):
    @abstractmethod
    async def get(self, id: str) -> Optional[T]: ...

    @abstractmethod
    async def list(self) -> Iterable[T]: ...

class BaseWriteOnlyRepository[T: BaseEntity](ABC):
    @abstractmethod
    async def create(self, entry: T) -> T: ...

    @abstractmethod
    async def create_empty(self) -> T: ...

    @abstractmethod
    async def delete(self, id: str) -> bool: ...

    @abstractmethod
    async def upsert(self, entry: T) -> T: ...

class BaseRepository[T: BaseEntity](
    BaseReadOnlyRepository[T],
    BaseWriteOnlyRepository[T],
    ABC,
): ...
