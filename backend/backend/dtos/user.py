from typing import TypedDict
from math import inf
from pydantic import BaseModel, computed_field

UserProfilePict = TypedDict('UserProfilePict', {
    'url': str,
    'height': int,
    'width': int,
})

class SpotifyUser(BaseModel):
    id: str
    images: list[UserProfilePict]
    display_name: str
    email: str

    @computed_field
    @property
    def avatar(self) -> str | None:
        if len(self.images) == 0:
            return None

        index = 0
        min_size = inf
        for i, image in enumerate(self.images):
            if image['width'] < min_size:
                index = i

        return self.images[index]['url']

    @property
    def as_user_info(self):
        return UserInfo.model_validate(
            self.model_dump(include={ 'avatar', 'display_name' }),
        )

class UserInfo(BaseModel):
    avatar: str | None
    display_name: str
