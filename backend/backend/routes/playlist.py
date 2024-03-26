from fastapi import APIRouter, Depends
from entities.user import UserEntity
from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from use_cases.playlist.get_spotify_playlists import GetSpotifyPlaylistsUseCase
from dtos.playlist import Playlists
from utils.fast_api_users_spotify import current_active_user

_repo = SpotifyPlaylistRepository()
_use_case = GetSpotifyPlaylistsUseCase(_repo)

router = APIRouter(
    prefix='/playlists',
    tags=['playlist'],
)

@router.get('', response_model=Playlists)
async def get_playlists(
    offset: int = 0,
    user: UserEntity = Depends(current_active_user),
):
    return await _use_case.execute(user, offset)
