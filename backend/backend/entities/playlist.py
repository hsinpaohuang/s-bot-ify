from typing import Optional, TYPE_CHECKING
from datetime import datetime
from pydantic import Field, BaseModel
from beanie import PydanticObjectId, BackLink
from entities.base_entity import BaseEntity

# circular import workaround
if TYPE_CHECKING:
    from entities.user import UserEntity

class ChatHistory(BaseModel):
    id: Optional[PydanticObjectId]
    bot: bool
    timestamp: datetime
    content: str

class PlaylistEntity(BaseEntity):
    user: BackLink['UserEntity'] = Field(original_field='playlists') # pyright:ignore
    chat_state: dict[str, str | int | float]
    history: list[ChatHistory]

    class Settings:
        name = 'playlists'

