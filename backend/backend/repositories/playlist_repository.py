from typing import Any, cast
from beanie import PydanticObjectId
from beanie.operators import LT
from repositories.base_repository import BaseRepository
from entities.playlist import PlaylistEntity
from dtos.playlist import PlaylistChatOnly

class PlaylistRepository(BaseRepository[PlaylistEntity]):
    async def get(self, id: str, args: dict[str, Any]):
        playlist = PlaylistEntity.find(
            PlaylistEntity.id == id,
            # PlaylistEntity.user.id doesn't work
            # ref: https://github.com/BeanieODM/beanie/issues/165
            { 'user.$id': PydanticObjectId(args['user_id']) },
        )

        # before
        before = args.get('before')
        if before:
            # Mongodb's ObjectID is always incremental, so we can use it to query lt/gt
            # ref: https://medium.com/swlh/mongodb-pagination-fast-consistent-ece2a97070f3
            playlist.find(LT(PlaylistEntity.history, before))
            playlist = cast(PlaylistEntity, playlist.project(PlaylistChatOnly))

        return cast(PlaylistEntity | None, await playlist.first_or_none())

    async def list(self): ...

    async def create(self): ...

    async def create_empty(self): ...

    async def delete(self): ...

    async def upsert(self): ...

    async def update(self): ...
