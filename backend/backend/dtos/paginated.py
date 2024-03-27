from pydantic import BaseModel, Field, computed_field

class SpotifyPaginated[T: BaseModel](BaseModel):
    next: str | None = Field(...)
    offset: int
    items: list[T]

    @computed_field
    @property
    def has_more(self) -> bool:
        return bool(self.next)


class Paginated(BaseModel):
    has_more: bool
    offset: int
