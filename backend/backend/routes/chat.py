from typing import Annotated
from fastapi import APIRouter, Depends
from dtos.chat import NewMessage
from repositories.playlist import PlaylistRepository
from repositories.playlist.beanie_playlist_repository import (
    BeaniePlaylistRepository
)
from repositories.user import UserRepository
from repositories.user.beanie_user_repository import (
    BeanieUserRepository
)
from use_cases.playlist.get_chat_messages_of_playlist import (
    GetChatMessageOfPlaylistUseCase,
)
from use_cases.playlist.get_playlist import GetPlaylistUseCase
from use_cases.playlist.create_playlist import CreatePlaylistUseCase
from use_cases.playlist.send_message import SendMessageUseCase
from dtos.playlist import PlaylistChatOnly
from utils.fast_api_users_spotify import CurrentActiveUserDep

# init repositories

def _init_playlist_repo():
    return BeaniePlaylistRepository()

_PlaylistRepoDep = Annotated[PlaylistRepository, Depends(_init_playlist_repo)]

def _init_user_repo():
    return BeanieUserRepository()

_UserRepoDep = Annotated[UserRepository, Depends(_init_user_repo)]

# init use cases

def _init_get_chat_messages_of_playlist_use_case(
    playlist_repo: _PlaylistRepoDep,
):
    return GetChatMessageOfPlaylistUseCase(playlist_repo)

_GetChatMessagesOfPlaylistUseCaseDep = Annotated[
    GetChatMessageOfPlaylistUseCase,
    Depends(_init_get_chat_messages_of_playlist_use_case),
]

def _init_create_playlist_use_case(
    playlist_repo: _PlaylistRepoDep,
    user_repo: _UserRepoDep,
):
    return CreatePlaylistUseCase(playlist_repo, user_repo)

def _init_get_playlist_use_case(
    playlist_repo: _PlaylistRepoDep,
    user_repo: _UserRepoDep,
):
    create_playlist_use_case = _init_create_playlist_use_case(
        playlist_repo,
        user_repo,
    )

    return GetPlaylistUseCase(playlist_repo, create_playlist_use_case)

def _init_send_message_use_case(
    playlist_repo: _PlaylistRepoDep,
    user_repo: _UserRepoDep,
):
    get_playlist_use_case = _init_get_playlist_use_case(
        playlist_repo,
        user_repo,
    )

    return SendMessageUseCase(playlist_repo, get_playlist_use_case)

_SendMessageUseCaseDep = Annotated[
    SendMessageUseCase,
    Depends(_init_send_message_use_case),
]

# router

router = APIRouter(
    prefix='/playlists',
    tags=['chat'],
)

@router.get(
    '/{playlist_id}/chat',
    response_model=PlaylistChatOnly,
)
async def get_chat_of_playlist(
    user: CurrentActiveUserDep,
    get_chat_message_of_playlist_use_case: _GetChatMessagesOfPlaylistUseCaseDep,
    playlist_id: str,
    before: str | None = None,
):
    return await get_chat_message_of_playlist_use_case \
        .execute(user, playlist_id, before)

@router.post('/{playlist_id}/chat')
async def send_message(
    user: CurrentActiveUserDep,
    send_message_use_case: _SendMessageUseCaseDep,
    playlist_id: str,
    message: NewMessage,
):
    await send_message_use_case.execute(playlist_id, user, message)
