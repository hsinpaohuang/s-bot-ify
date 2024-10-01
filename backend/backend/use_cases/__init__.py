from abc import ABCMeta, abstractmethod

# ref: https://medium.com/@shaliamekh/clean-architecture-with-python-d62712fd8d4f

class BaseUseCase(metaclass=ABCMeta):
    @abstractmethod
    async def execute(self, *args, **kwargs): # pyright:ignore
        ...
