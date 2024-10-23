import requests as re
from datetime import datetime, timedelta
from typing import Literal, Any, TypedDict
import urllib.parse

Song = TypedDict('Song', {
    'name': str,
    'artists': list[str],
    'url': str,
})

class _SpotifyAPI():
    _SPOTIFY_API_BASE_URL = 'https://api.spotify.com'

    def __init__(self):
        self._token_expire_time = datetime.now()

        # with open('envs.json', 'r', encoding='utf-8') as envs:
        #     secrets = json.load(envs)
        # self._client_id = secrets['client_id']
        # self._client_secret = secrets['client_secret']

    def search(self, query: str, search_type: Literal['name', 'genre'], artist: str, page: int):
        # reference: https://developer.spotify.com/documentation/web-api/reference/search

        if search_type == 'genre':
            search_query = f"genre:{query}"
        else:
            search_query = query

        if artist:
            search_query += f" artist:{artist}"

        search_params = {
            'q': urllib.parse.quote(search_query),
            'type': 'track',
            'limit': 5,
        }
        if page > 1:
            search_params['offset'] = 5 * (page - 1)

        data = self._request('/v1/search', 'get', search_params)
        return self._process_data(data)

    def _authenticate(self):
        # reference: https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow
        res = re.post(
            'https://accounts.spotify.com/api/token',
            {
                'grant_type': 'client_credentials',
                'client_id': self._client_id,
                'client_secret': self._client_secret,
            },
            headers={ 'Content-Type': 'application/x-www-form-urlencoded' }
        )

        if res.status_code != 200:
            raise RuntimeError('Failed to authenticate with Spotify API server. Please try again later.')

        token_data = res.json()
        self._access_token = token_data['access_token']
        self._token_expire_time = datetime.now() + timedelta(seconds=token_data['expires_in'] - 1)
        self._token_type = token_data['token_type']

    def _request(self, endpoint: str, method: Literal['get', 'post'], params: dict[str, Any]):
        # check if token has expired, if yes, get a new one
        if self._token_expire_time < datetime.now():
            self._authenticate()

        url = f'{self._SPOTIFY_API_BASE_URL}{endpoint}'
        headers = { 'Authorization': f'{self._token_type} {self._access_token}' }

        if method == 'get':
            res = re.get(url, params, headers=headers)
        elif method == 'post':
            res = re.post(url, params, headers=headers)

        if res.status_code != 200:
            raise RuntimeError('Something went wrong. Please try again later')

        return res.json()

    def _process_data(self, data: Any):
        results = list[Song]()
        for track in data['tracks']['items']:
            results.append({
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'url': track['external_urls']['spotify'],
            })

        return results

spotify_api = _SpotifyAPI()
