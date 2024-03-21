from abc import ABCMeta, abstractmethod

# reference: https://fueled.com/the-cache/posts/backend/clean-architecture-with-fastapi/

class BaseUseCase(metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, *args, **kwargs): # pyright:ignore
        ...
