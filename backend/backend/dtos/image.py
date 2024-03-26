from math import inf
from pydantic import BaseModel, Field, computed_field

class SpotifyImage(BaseModel):
    url: str
    height: int | None = Field(...)
    width: int | None = Field(...)

class SpotifyImages(BaseModel):
    images: list[SpotifyImage] | None = Field(...)

    @computed_field
    @property
    def icon(self) -> str | None:
        if not self.images:
            return None

        index = 0
        min_size = inf
        for i, image in enumerate(self.images):
            if not image.width or image.width < min_size:
                index = i

        return self.images[index].url
