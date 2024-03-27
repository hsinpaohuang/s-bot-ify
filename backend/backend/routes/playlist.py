from fastapi import APIRouter, Depends
from entities.user import UserEntity
from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from repositories.spotify.track_repository import TrackRepository
from use_cases.playlist.get_spotify_playlists import GetSpotifyPlaylistsUseCase
from use_cases.playlist.get_spotify_tracks_of_playlist import (
    GetSpotifyTracksOfPlaylistUseCase,
)
from dtos.playlist import Playlists
from dtos.track import Tracks
from utils.fast_api_users_spotify import current_active_user

_playlist_repo = SpotifyPlaylistRepository()
_track_repo = TrackRepository()
_get_spotify_play_list_use_case = GetSpotifyPlaylistsUseCase(_playlist_repo)
_get_spotify_tracks_of_playlist_use_case = GetSpotifyTracksOfPlaylistUseCase(
    _track_repo,
)

router = APIRouter(
    prefix='/playlists',
    tags=['playlist'],
)

@router.get('', response_model=Playlists)
async def get_playlists(
    offset: int = 0,
    user: UserEntity = Depends(current_active_user),
):
    return await _get_spotify_play_list_use_case.execute(user, offset)

@router.get('/{playlist_id}/tracks', response_model=Tracks, tags=['tracks'])
async def get_tracks_of_playlist(
    playlist_id: str,
    offset: int = 0,
    user: UserEntity = Depends(current_active_user),
):
    return await _get_spotify_tracks_of_playlist_use_case \
        .execute(user, playlist_id, offset)
