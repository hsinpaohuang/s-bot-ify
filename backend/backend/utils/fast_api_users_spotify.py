from typing import Optional
from fastapi import Request, Depends
from beanie import PydanticObjectId
from httpx_oauth.oauth2 import OAuth2
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from entities.user import UserEntity, OAuthAccount
from repositories.spotify.user_repository import SpotifyUserRepository
from use_cases.user.get_spotify_user_use_case import GetSpotifyUserUseCase
from utils.env import settings

# reference: https://fastapi-users.github.io/fastapi-users/latest/configuration/oauth/#beanie_1

_spotify_user_repo = SpotifyUserRepository()

# reference: https://github.com/frankie567/httpx-oauth/issues/103#issuecomment-633380615
class _SpotifyOAuth(OAuth2):
    async def get_id_email(self, token: str):
        user = await GetSpotifyUserUseCase(_spotify_user_repo).execute(token)
        return user.id, user.email

oauth_client = _SpotifyOAuth(
     client_id=settings.spotify_client_id,
     client_secret=settings.spotify_client_secret,
     authorize_endpoint='https://accounts.spotify.com/authorize',
     access_token_endpoint='https://accounts.spotify.com/api/token',
     refresh_token_endpoint='https://accounts.spotify.com/api/token',
     base_scopes=['user-read-email'],
)

class _UserManager(ObjectIDIDMixin, BaseUserManager[UserEntity, PydanticObjectId]):
    async def on_after_register(self, user: UserEntity, _: Optional[Request] = None):
        print(f"User {user.id} has registered.")

async def _get_user_db(): # pyright:ignore
    yield BeanieUserDatabase(UserEntity, OAuthAccount) # pyright:ignore

async def __get_user_manager(
    user_db: BeanieUserDatabase[UserEntity] = Depends(_get_user_db) # pyright:ignore
):
    yield _UserManager(user_db)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=BearerTransport(tokenUrl="auth/jwt/login"),
    get_strategy=lambda: JWTStrategy(
        secret=settings.spotify_jwt_secret,
        lifetime_seconds=3600
    ), # pyright:ignore
)

fastapi_users = FastAPIUsers[UserEntity, PydanticObjectId](
    get_user_manager=__get_user_manager,
    auth_backends=[auth_backend],
)
