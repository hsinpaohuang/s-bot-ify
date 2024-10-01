from .. import BaseUseCase
from entities.user import UserEntity
from entities.playlist import PlaylistEntity
from repositories.playlist import PlaylistRepository
from use_cases.playlist.create_playlist import CreatePlaylistUseCase


class GetPlaylistUseCase(BaseUseCase):
    def __init__(
            self,
            repo: PlaylistRepository,
            create_playlist_use_case: CreatePlaylistUseCase,
        ):
        self._repo = repo
        self._create_playlist_use_case = create_playlist_use_case

    async def execute(
        self,
        playlist_id: str,
        user: UserEntity,
    ) -> PlaylistEntity:
        playlist = await self._repo.get(playlist_id, user)

        if playlist == None:
            playlist = await self._create_playlist_use_case \
                .execute(playlist_id, user)

        return playlist
