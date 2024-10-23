from typing import Annotated
from fastapi import APIRouter, Depends
from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from repositories.spotify.track_repository import SpotifyTrackRepository
from use_cases.playlist.get_spotify_playlists import GetSpotifyPlaylistsUseCase
from use_cases.playlist.get_spotify_tracks_of_playlist import (
    GetSpotifyTracksOfPlaylistUseCase,
)
from dtos.playlist import Playlists
from dtos.track import Tracks
from utils.fast_api_users_spotify import CurrentActiveUserDep

# init repositories

def _init_spotify_playlist_repo():
    return SpotifyPlaylistRepository()

_SpotifyPlaylistRepoDep = Annotated[
    SpotifyPlaylistRepository,
    Depends(_init_spotify_playlist_repo),
]

def _init_spotify_track_repo():
    return SpotifyTrackRepository()

_TrackRepoDep = Annotated[
    SpotifyTrackRepository,
    Depends(_init_spotify_track_repo),
]

# init use cases

def _init_get_spotity_playlists_use_case(
    spotify_playlist_repo: _SpotifyPlaylistRepoDep,
):
    return GetSpotifyPlaylistsUseCase(spotify_playlist_repo)

_GetSpotifyPlaylistsUseCaseDep = Annotated[
    GetSpotifyPlaylistsUseCase,
    Depends(_init_get_spotity_playlists_use_case),
]

def _init_get_spotify_tracks_of_playlist_use_case(
    track_repo: _TrackRepoDep,
):
    return GetSpotifyTracksOfPlaylistUseCase(track_repo)

_GetSpotifyTracksOfPlaylistUseCaseDep = Annotated[
    GetSpotifyTracksOfPlaylistUseCase,
    Depends(_init_get_spotify_tracks_of_playlist_use_case),
]

# routes

router = APIRouter(
    prefix='/playlists',
    tags=['playlist'],
)

@router.get('', response_model=Playlists)
async def get_playlists(
    user: CurrentActiveUserDep,
    get_spotify_playlists_use_case: _GetSpotifyPlaylistsUseCaseDep,
    offset: int = 0,
):
    return await get_spotify_playlists_use_case.execute(user, offset)

@router.get('/{playlist_id}/tracks', response_model=Tracks, tags=['tracks'])
async def get_tracks_of_playlist(
    user: CurrentActiveUserDep,
    get_spotify_tracks_of_playlist_use_case: _GetSpotifyTracksOfPlaylistUseCaseDep,
    playlist_id: str,
    offset: int = 0,
):
    return await get_spotify_tracks_of_playlist_use_case \
        .execute(user, playlist_id, offset)
