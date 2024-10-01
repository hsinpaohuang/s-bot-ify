from abc import ABC, abstractmethod
from entities.user import UserEntity
from entities.playlist import PlaylistEntity, ChatHistory
from dtos.playlist import PlaylistChatOnly

class PlaylistRepository(ABC):
    @abstractmethod
    async def get(
        self,
        id: str,
        user: UserEntity,
        before: str | None = None,
    ) -> PlaylistEntity | None: ...

    @abstractmethod
    async def get_messages(
        self,
        playlist: PlaylistEntity,
        before: str | None = None,
    ) -> PlaylistChatOnly: ...

    @abstractmethod
    async def add_message(
        self,
        playlist: PlaylistEntity,
        message: ChatHistory,
    ) -> ChatHistory: ...
