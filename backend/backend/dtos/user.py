from pydantic import BaseModel, Field
from dtos.image import SpotifyImages

class SpotifyUser(SpotifyImages, BaseModel):
    id: str
    display_name: str
    email: str

    @property
    def as_user_info(self):
        return UserInfo.model_validate(
            self.model_dump(include={ 'icon', 'display_name' }),
        )

class UserInfo(BaseModel):
    icon: str | None = Field(...)
    display_name: str
