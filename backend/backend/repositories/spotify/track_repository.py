from typing import Literal
from urllib.parse import quote
from entities.user import UserEntity
from dtos.track import SpotifyTracks, SpotifySearchResult
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

    async def search(
        self,
        user: UserEntity,
        query: str,
        search_type: Literal['name', 'genre'],
        artist: str,
        page: int = 0,
    ):
        # reference: https://developer.spotify.com/documentation/web-api/reference/search

        if search_type == 'genre':
            search_query = f"genre:{query}"
        else:
            search_query = query

        if artist:
            search_query += f' artist:{artist}'

        search_params = {
            'q': quote(search_query),
            'type': 'track',
            'limit': '5',
        }

        if page > 1:
            search_params['offset'] = str(5 * (page - 1))

        return await SpotifyAPI(user).get(
            '/v1/search',
            SpotifySearchResult,
            params=search_params,
        )
