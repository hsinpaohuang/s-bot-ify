from beanie.operators import Push
from .. import BaseUseCase
from entities.user import UserEntity
from entities.playlist import PlaylistEntity
from repositories.playlist import PlaylistRepository
from repositories.user import UserRepository

class CreatePlaylistUseCase(BaseUseCase):
    def __init__(
        self,
        playlist_repo: PlaylistRepository,
        user_repo: UserRepository
    ):
        self._playlist_repo = playlist_repo
        self._user_repo = user_repo

    async def execute(self, playlist_id: str, user: UserEntity) -> PlaylistEntity:
        playlist = await self._playlist_repo.create(playlist_id, user)

        await user.update(Push({ UserEntity.playlists: playlist.to_ref() })) # pyright: ignore

        return playlist


