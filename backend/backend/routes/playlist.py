from fastapi import APIRouter, Depends
from dtos.chat import NewMessage
from entities.user import UserEntity
from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from repositories.spotify.track_repository import TrackRepository
from repositories.playlist_repository import PlaylistRepository
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
from utils.fast_api_users_spotify import current_active_user

_spotify_playlist_repo = SpotifyPlaylistRepository()
_track_repo = TrackRepository()
_playlist_repo = PlaylistRepository()
_get_spotify_play_list_use_case = GetSpotifyPlaylistsUseCase(_spotify_playlist_repo)
_get_spotify_tracks_of_playlist_use_case = GetSpotifyTracksOfPlaylistUseCase(
    _track_repo,
)
_get_chat_messages_of_playlist = GetChatMessageOfPlaylistUseCase(
    _playlist_repo,
)
_get_playlist_use_case = GetPlaylistUseCase(_playlist_repo)
_create_playlist_use_case = CreatePlaylistUseCase(_playlist_repo)
_send_message_use_case = SendMessageUseCase(_playlist_repo)

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

@router.get('/{playlist_id}/chat', response_model=PlaylistChatOnly, tags=['chat'])
async def get_chat_of_playlist(
    playlist_id: str,
    before: str | None = None,
    user: UserEntity = Depends(current_active_user),
):
    return await _get_chat_messages_of_playlist \
        .execute(user, playlist_id, before)

@router.post('/{playlist_id}/chat', tags=['chat'])
async def send_message(
        playlist_id: str,
        message: NewMessage,
        user: UserEntity = Depends(current_active_user)
):
    playlist = await _get_playlist_use_case.execute(playlist_id, user)
    if playlist == None:
        playlist = await _create_playlist_use_case.execute(playlist_id, user)

    await _send_message_use_case.execute(playlist, message)
