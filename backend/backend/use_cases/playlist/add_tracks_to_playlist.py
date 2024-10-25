from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from entities.user import UserEntity

class AddTracksToPlaylistUseCase:
    def __init__(self, spotify_playlist_repository: SpotifyPlaylistRepository):
        self.spotify_playlist_repository = spotify_playlist_repository

    async def execute(
        self,
        user: UserEntity,
        playlist_id: str,
        track_uris: list[str],
    ):
        await self.spotify_playlist_repository.add_tracks(
            user,
            playlist_id,
            track_uris,
        )
