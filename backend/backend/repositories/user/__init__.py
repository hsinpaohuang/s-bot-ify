from abc import ABC, abstractmethod
from entities.user import UserEntity
from dtos.spotify_token import SpotifyToken

class UserRepository(ABC):
    @abstractmethod
    async def update_token(
        self,
        user: UserEntity,
        token: SpotifyToken,
    ) -> UserEntity:
        ...
