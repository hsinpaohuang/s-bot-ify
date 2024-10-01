from typing import Annotated
from fastapi import APIRouter, Depends
from use_cases.user.get_spotify_user_use_case import GetSpotifyUserUseCase
from repositories.spotify.user_repository import SpotifyUserRepository
from dtos.user import UserInfo
from utils.fast_api_users_spotify import CurrentActiveUserDep

_user_repo = SpotifyUserRepository()
_use_case = GetSpotifyUserUseCase(_user_repo)

def _init_spotify_user_repo():
    return SpotifyUserRepository()

_SpotifyUserRepoDep = Annotated[
    SpotifyUserRepository,
    Depends(_init_spotify_user_repo),
]

def _init_get_spotify_user_use_case(
    spotify_user_repo: _SpotifyUserRepoDep,
):
    return GetSpotifyUserUseCase(spotify_user_repo)

_GetSpotifyUserUseCaseDep = Annotated[
    GetSpotifyUserUseCase,
    Depends(_init_get_spotify_user_use_case),
]

router = APIRouter(
    prefix='/users',
    tags=['user'],
    responses={ 404: { 'detail': 'Not found' } },
)

@router.get('/me', response_model=UserInfo)
async def user_info(
    user: CurrentActiveUserDep,
    get_spotify_user_use_case: _GetSpotifyUserUseCaseDep,
):
    spotify_user = await get_spotify_user_use_case.execute(user)

    return spotify_user.as_user_info
