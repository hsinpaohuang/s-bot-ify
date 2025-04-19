from pydantic import BaseModel, Field
from dtos.image import SpotifyImages
from dtos.paginated import SpotifyPaginated, Paginated
from dtos.chat import ChatMessage
from entities.playlist import ChatHistory

class SpotifyEntityOwner(BaseModel):
    id: str

class SpotifyPlaylist(SpotifyImages, BaseModel):
    id: str
    name: str
    owner: SpotifyEntityOwner

class SpotifyPlaylists(SpotifyPaginated[SpotifyPlaylist], BaseModel):
    def editable_playlists(self, user_id: str):
        return [item for item in self.items if item.owner.id == user_id]

    def to_playlists(self, user_id: str):
        output = self.model_dump(include={ 'offset', 'has_more', 'total' })
        output['playlists'] = [
            Playlist.model_validate(
                item.model_dump(include={ 'id', 'icon', 'name' }),
            )
            for item in self.editable_playlists(user_id)
        ]

        return Playlists.model_validate(output)

class Playlist(BaseModel):
    id: str
    icon: str | None = Field(...)
    name: str

class Playlists(Paginated, BaseModel):
    playlists: list[Playlist]

class PlaylistChatOnly(BaseModel):
    history: list[ChatHistory] = Field(default_factory=list)

    def convert(self):
        return [ChatMessage.from_chat_history(h) for h in self.history]

    class Settings:
        projection = { 'history': { '$slice': ['$history', -10] } }
