from fastapi import APIRouter, Depends
from entities.user import UserEntity
from use_cases.user.get_spotify_user_use_case import GetSpotifyUserUseCase
from repositories.spotify.user_repository import SpotifyUserRepository
from dtos.user import UserInfo
from utils.fast_api_users_spotify import current_active_user

_user_repo = SpotifyUserRepository()
_use_case = GetSpotifyUserUseCase(_user_repo)

router = APIRouter(
    prefix='/users',
    tags=['user'],
    responses={ 404: { 'detail': 'Not found' } },
)

@router.get('/me', response_model=UserInfo)
async def user_info(user: UserEntity = Depends(current_active_user)):
    spotify_user = await _use_case.execute(user)

    return spotify_user.as_user_info
