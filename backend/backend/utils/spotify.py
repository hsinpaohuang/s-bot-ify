from typing import Type, overload, Any
from pydantic import BaseModel
from entities.user import UserEntity
from utils.aiohttp_session import session
from repositories.user.beanie_user_repository import BeanieUserRepository
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
            params: dict[str, str] | None = None,
        ) -> T:
        await self._check_token()

        parsed_path = path.lstrip('/')

        async with session.get(
            f'{self._SPOTIFY_API_V1_URL}/{parsed_path}',
            headers=self._header,
            params=params,
        ) as resp:
            result = await resp.json()

            if not resp.ok:
                raise RuntimeError(
                    f'Failed to get {path}: {result['error']['message']}',
                )

            return result_model.model_validate(result)

    @overload
    async def post(
        self,
        path: str,
        result_model: None,
        data: dict[str, Any] | None = None,
    ) -> None: ...

    @overload
    async def post[T: BaseModel](
        self,
        path: str,
        result_model: Type[T],
        data: dict[str, Any] | None = None,
    ) -> T: ...

    async def post[T: BaseModel](
        self,
        path: str,
        result_model: Type[T] | None,
        data: dict[str, Any] | None = None,
    ) -> T | None:
        await self._check_token()

        parsed_path = path.lstrip('/')

        async with session.post(
            f'{self._SPOTIFY_API_V1_URL}/{parsed_path}',
            headers=self._header,
            json=data,
        ) as resp:
            result = await resp.json()

            if not resp.ok:
                raise RuntimeError(
                    f'Failed to post {path}: {result['error']['message']}',
                )

            if result_model:
                return result_model.model_validate(result)

    async def _check_token(self):
        if not self._user:
            return

        if self._user.is_token_expired:
            await self._refresh_access_token()

    async def _refresh_access_token(self):
        if not self._user:
            return

        refresh_token = self._user.oauth_accounts[0].refresh_token

        if not refresh_token:
            raise ValueError('Refresh token missing')

        # importing here to prevent circular import
        from utils.fast_api_users_spotify import oauth_client
        tokens = SpotifyToken.model_validate(
            await oauth_client.refresh_token(refresh_token)
        )

        repo = BeanieUserRepository()
        update_access_token_use_case = UpdateAccessTokenUseCase(repo)
        self._user = await update_access_token_use_case \
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
