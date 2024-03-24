from typing import Type
from base64 import b64encode
from fastapi import status
from pydantic import BaseModel
from entities.user import UserEntity
from utils.aiohttp_session import session
from utils.env import settings
from repositories.spotify.token_repository import SpotifyTokenRepository
from use_cases.user.update_access_token_use_case import UpdateAccessTokenUseCase
from dtos.spotify_token import SpotifyToken

class SpotifyAPI():
    _SPOTIFY_API_V1_URL = 'https://api.spotify.com'
    _SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    _user: UserEntity | None

    def __init__(
            self,
            user: UserEntity | None = None,
            access_token: str | None = None
        ):
        self._user = user
        self._input_access_token = access_token

    async def get[T: BaseModel](
            self,
            path: str,
            result_model: Type[T],
            check_token: bool=True
        ) -> T:
        is_token_checked = False

        if check_token:
            await self._check_token()
            is_token_checked = True

        parsed_path = path.lstrip('/')

        async with session.get(
            f'{self._SPOTIFY_API_V1_URL}/{parsed_path}',
            headers=self._header,
        ) as resp:
            result = await resp.json()

            if not resp.ok:
                if resp.status == status.HTTP_401_UNAUTHORIZED \
                    and not is_token_checked:
                    return await self.get(path, result_model)
                else:
                    raise RuntimeError(
                        f'Failed to get {path}: {result['error']['message']}',
                    )

            return result_model.model_validate(result)

    async def _check_token(self):
        if not self._user:
            return True

        if self._user.is_token_expired:
            await self._refresh_access_token()

    async def _refresh_access_token(self):
        if not self._user:
            return

        auth_header = b64encode(
            f'{settings.spotify_client_id}:{settings.spotify_client_secret}' \
            .encode(),
        )
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': auth_header,
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._user.oauth_accounts[0].refresh_token,
        }

        async with session.post(
            self._SPOTIFY_TOKEN_URL,
            headers=headers,
            data=data,
        ) as resp:
            if not resp.ok:
                raise RuntimeError('Failed to refresh token')

            tokens = SpotifyToken.model_validate(await resp.json())
            repo = SpotifyTokenRepository()
            self._user = await UpdateAccessTokenUseCase(repo) \
                .execute(self._user, tokens)

    @property
    def _access_token(self):
        if self._user:
            return self._user.oauth_accounts[0].access_token

        if self._input_access_token:
            return self._input_access_token

        raise ValueError('No access token provided')

    @property
    def _header(self):
        return { 'Authorization': f'Bearer {self._access_token}' }
