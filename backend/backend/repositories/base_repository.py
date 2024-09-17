from typing import Optional, Iterable, overload, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel
from entities.base_entity import BaseEntity

# reference: https://fueled.com/the-cache/posts/backend/clean-architecture-with-fastapi/
# TODO: use default generic in python 3.13

class BaseReadOnlyRepository[T: BaseEntity](ABC):
    @abstractmethod
    @overload
    async def get(self, id: str, conditions: Any = None) -> Optional[T]: ...

    @abstractmethod
    @overload
    async def get(self, condition: Any) -> Optional[T]: ...

    @abstractmethod
    async def list(self, **kwargs: Any) -> Iterable[T]: ...

class BaseWriteOnlyRepository[T: BaseEntity](ABC):
    @abstractmethod
    async def create(self, entry: T) -> T: ...

    @abstractmethod
    async def create_empty(self) -> T: ...

    @abstractmethod
    async def delete(self, id: str) -> bool: ...

    @abstractmethod
    async def upsert(self, entry: T) -> T: ...

    @abstractmethod
    async def update(self, entity: T, updates: BaseModel) -> T: ...

class BaseRepository[T: BaseEntity](
    BaseReadOnlyRepository[T],
    BaseWriteOnlyRepository[T],
    ABC,
): ...
