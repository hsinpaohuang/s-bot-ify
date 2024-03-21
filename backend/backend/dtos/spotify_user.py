from typing import TypedDict
from math import inf
from pydantic import BaseModel
# from entities.user import UserEntity

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

    # @property
    # def as_user_entity(self):
    #     return UserEntity(
    #         spotify_id=self.id,
    #         avatar=self._avatar,
    #         name=self.display_name,
    #         email=self.email,
    #     )

    @property
    def _avatar(self):
        if len(self.images) == 0:
            return None

        index = 0
        min_size = inf
        for i, image in enumerate(self.images):
            if image['width'] < min_size:
                index = i

        return self.images[index]['url']

