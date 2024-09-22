from beanie import Link
from beanie.operators import Push
from use_cases.base_use_case import BaseUseCase
from entities.user import UserEntity
from entities.playlist import PlaylistEntity
from repositories.playlist_repository import PlaylistRepository

class CreatePlaylistUseCase(BaseUseCase):
    def __init__(self, repo: PlaylistRepository):
        self._repo = repo

    async def execute(self, playlist_id: str, user: UserEntity) -> PlaylistEntity:
        playlist = await PlaylistEntity(
            spotify_playlist_id = playlist_id,
            user = Link(user.to_ref(), UserEntity),
        ).create()

        await user.update(Push({ UserEntity.playlists: playlist.to_ref() }))

        return playlist


