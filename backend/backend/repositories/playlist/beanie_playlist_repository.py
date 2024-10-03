from typing import cast
from beanie import Link, PydanticObjectId
from beanie.operators import LT, Push
from . import PlaylistRepository
from entities.playlist import ChatHistory, PlaylistEntity
from entities.user import UserEntity
from dtos.playlist import PlaylistChatOnly

class BeaniePlaylistRepository(PlaylistRepository):
    async def create(self, spotify_playlist_id: str, user: UserEntity):
        return await PlaylistEntity(
            spotify_playlist_id = spotify_playlist_id,
            user = Link(user.to_ref(), UserEntity),
        ).create()

    async def get(self, id: str, user: UserEntity, before: str | None = None):
        playlist = PlaylistEntity.find(
            # avoid using id, use spotify_playlist_id instead
            PlaylistEntity.spotify_playlist_id == id,
            # PlaylistEntity.user.id doesn't work...?
            # ref: https://github.com/BeanieODM/beanie/issues/165
            PlaylistEntity.user.id == user.id, # pyright:ignore
        )

        if before:
            # Mongodb's ObjectID is always incremental, so we can use it to query lt/gt
            # ref: https://medium.com/swlh/mongodb-pagination-fast-consistent-ece2a97070f3
            playlist.find(LT(PlaylistEntity.history, before))
            playlist = cast(PlaylistEntity, playlist.project(PlaylistChatOnly))

        return cast(PlaylistEntity | None, await playlist.first_or_none())

    async def get_messages(
        self,
        playlist_id: str,
        user: UserEntity,
        before: str | None = None,
    ) -> PlaylistChatOnly | None:
        # Mongodb's ObjectID is always incremental, so we can use it to query lt/gt
        # ref: https://medium.com/swlh/mongodb-pagination-fast-consistent-ece2a97070f3
        playlist = PlaylistEntity.find(
            PlaylistEntity.spotify_playlist_id == playlist_id,
            PlaylistEntity.user.id == user.id, # pyright:ignore
        )

        if before:
            playlist = playlist.aggregate(
                [{
                    '$project': {
                        'history': { '$filter': {
                            'input': '$history',
                            'as': 'item',
                            'cond': { '$lt': [
                                '$$item.id',
                                PydanticObjectId(before),
                            ]},
                        }},
                    }
                }],
                projection_model=PlaylistChatOnly,
            )

            res = (await playlist.to_list())[0]
        else:
            playlist = playlist.project(PlaylistChatOnly)
            res = await playlist.first_or_none()

        return res

    async def add_message(self, playlist: PlaylistEntity, message: ChatHistory):
        updated_playlist = cast(PlaylistEntity, await playlist.update(
            Push({ PlaylistEntity.history: message }), # pyright: ignore
        ))

        return next(
            (i for i in updated_playlist.history if i.id == message.id),
            message,
        )
