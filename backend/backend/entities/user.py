from typing import TYPE_CHECKING
from datetime import datetime
from time import mktime
from beanie import Link, PydanticObjectId
from pydantic import Field
from fastapi_users.db import BaseOAuthAccount, BeanieBaseUser
from entities.base_entity import BaseEntity
from entities.playlist import PlaylistEntity

# circular import workaround
if TYPE_CHECKING:
    from entities.playlist import PlaylistEntity

class OAuthAccount(BaseOAuthAccount):
    pass

class UserEntity(BeanieBaseUser, BaseEntity):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    oauth_accounts: list[OAuthAccount] = Field(default_factory=list)
    playlists: list[Link['PlaylistEntity']] = Field(default_factory=list)

    @property
    def spotify_id(self):
        return self.oauth_accounts[0].account_id

    @property
    def is_token_expired(self):
        if self.oauth_accounts[0].expires_at is None:
            return True

        now = mktime(datetime.now().timetuple())
        return int(now) > self.oauth_accounts[0].expires_at

    class Settings(BeanieBaseUser.Settings):
        name = 'users'
