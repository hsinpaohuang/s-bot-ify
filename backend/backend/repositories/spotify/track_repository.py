from entities.user import UserEntity
from dtos.track import SpotifyTracks
from utils.spotify import SpotifyAPI

class TrackRepository():
    async def list(
        self,
        user: UserEntity,
        playlist_id: str,
        offset: int = 0,
    ):
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
