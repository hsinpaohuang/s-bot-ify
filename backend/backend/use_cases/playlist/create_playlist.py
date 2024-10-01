from beanie import Link
from beanie.operators import Push
from .. import BaseUseCase
from entities.user import UserEntity
from entities.playlist import PlaylistEntity
from repositories.playlist import PlaylistRepository

class CreatePlaylistUseCase(BaseUseCase):
    def __init__(self, repo: PlaylistRepository):
        self._repo = repo

    async def execute(self, playlist_id: str, user: UserEntity) -> PlaylistEntity:
        playlist = await PlaylistEntity(
            spotify_playlist_id = playlist_id,
            user = Link(user.to_ref(), UserEntity),
        ).create()

        await user.update(Push({ UserEntity.playlists: playlist.to_ref() })) # pyright: ignore

        return playlist


