from typing import TYPE_CHECKING, Annotated, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from beanie import Indexed, PydanticObjectId, Link
import pymongo
from entities.base_entity import BaseEntity

# circular import workaround
if TYPE_CHECKING:
    from entities.user import UserEntity

class ChatHistory(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    bot: bool
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    content: str

class PlaylistEntity(BaseEntity):
    user: Link['UserEntity']
    spotify_playlist_id: Annotated[str, Indexed(index_type=pymongo.TEXT, unique=True)]
    chat_state: dict[str, Any] = Field(default_factory=dict)
    history: list[ChatHistory] = Field(default_factory=list)

    class Settings:
        name = 'playlists'

