from typing import Annotated
from fastapi import APIRouter, Depends
from dtos.chat import NewMessage
from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from repositories.spotify.track_repository import TrackRepository
from repositories.playlist import PlaylistRepository
from repositories.playlist.beanie_playlist_repository import (
    BeaniePlaylistRepository
)
from use_cases.playlist.get_spotify_playlists import GetSpotifyPlaylistsUseCase
from use_cases.playlist.get_spotify_tracks_of_playlist import (
    GetSpotifyTracksOfPlaylistUseCase,
)
from use_cases.playlist.get_chat_messages_of_playlist import (
    GetChatMessageOfPlaylistUseCase,
)
from use_cases.playlist.get_playlist import GetPlaylistUseCase
from use_cases.playlist.create_playlist import CreatePlaylistUseCase
from use_cases.playlist.send_message import SendMessageUseCase
from dtos.playlist import Playlists, PlaylistChatOnly
from dtos.track import Tracks
from utils.fast_api_users_spotify import CurrentActiveUserDep

# init repositories

def _init_spotify_playlist_repo():
    return SpotifyPlaylistRepository()

_SpotifyPlaylistRepoDep = Annotated[
    SpotifyPlaylistRepository,
    Depends(_init_spotify_playlist_repo),
]

def _init_track_repo():
    return TrackRepository()

_TrackRepoDep = Annotated[TrackRepository, Depends(_init_track_repo)]

def _init_playlist_repo():
    return BeaniePlaylistRepository()

_PlaylistRepoDep = Annotated[PlaylistRepository, Depends(_init_playlist_repo)]

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

def _init_get_chat_messages_of_playlist_use_case(
    playlist_repo: _PlaylistRepoDep,
):
    return GetChatMessageOfPlaylistUseCase(playlist_repo)

_GetChatMessagesOfPlaylistUseCaseDep = Annotated[
    GetChatMessageOfPlaylistUseCase,
    Depends(_init_get_chat_messages_of_playlist_use_case),
]

def _init_create_playlist_use_case(playlist_repo: _PlaylistRepoDep):
    return CreatePlaylistUseCase(playlist_repo)

def _init_get_playlist_use_case(playlist_repo: _PlaylistRepoDep):
    create_playlist_use_case = _init_create_playlist_use_case(playlist_repo)

    return GetPlaylistUseCase(playlist_repo, create_playlist_use_case)

def _init_send_message_use_case(playlist_repo: _PlaylistRepoDep):
    get_playlist_use_case = _init_get_playlist_use_case(playlist_repo)
    return SendMessageUseCase(playlist_repo, get_playlist_use_case),

_SendMessageUseCaseDep = Annotated[
    SendMessageUseCase,
    Depends(_init_send_message_use_case),
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

@router.get(
    '/{playlist_id}/chat',
    response_model=PlaylistChatOnly,
    tags=['chat'],
)
async def get_chat_of_playlist(
    user: CurrentActiveUserDep,
    get_chat_message_of_playlist_use_case: _GetChatMessagesOfPlaylistUseCaseDep,
    playlist_id: str,
    before: str | None = None,
):
    return await get_chat_message_of_playlist_use_case \
        .execute(user, playlist_id, before)

@router.post('/{playlist_id}/chat', tags=['chat'])
async def send_message(
        user: CurrentActiveUserDep,
        send_message_use_case: _SendMessageUseCaseDep,
        playlist_id: str,
        message: NewMessage,
):
    await send_message_use_case.execute(playlist_id, user, message)
