from repositories.base_repository import BaseRepository
from entities.base_entity import BaseEntity
from entities.user import UserEntity
from dtos.track import SpotifyTracks
from utils.spotify import SpotifyAPI

class TrackRepository(BaseRepository[BaseEntity]):
    async def list(
        self,
        user: UserEntity,
        playlist_id: str | None = None,
        offset: int = 0,
    ):
        if playlist_id:
            params = {
                'offset': str(offset),
                'limit': '20',
                'fields': 'next,offset,items(track(id,name,artists(name),album(images)))',
            }

            return await SpotifyAPI(user).get(
                f'/v1/playlists/{playlist_id}/tracks',
                SpotifyTracks,
                params=params,
            )

        raise NotImplementedError

    async def get(self): ...

    async def create(self): ...

    async def create_empty(self): ...

    async def delete(self): ...

    async def upsert(self): ...

    async def update(self): ...
