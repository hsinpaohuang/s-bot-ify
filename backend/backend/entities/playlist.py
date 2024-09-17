from typing import TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel, Field
from beanie import PydanticObjectId, Link
from entities.base_entity import BaseEntity

# circular import workaround
if TYPE_CHECKING:
    from entities.user import UserEntity

class ChatHistory(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    bot: bool
    timestamp: datetime
    content: str

class PlaylistEntity(BaseEntity):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    user: Link['UserEntity']
    chat_state: dict[str, str | int | float]
    history: list[ChatHistory]

    class Settings:
        name = 'playlists'

