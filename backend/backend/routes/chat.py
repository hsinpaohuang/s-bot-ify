from typing import Annotated
from asyncio import gather
from fastapi import APIRouter, Depends
from dtos.chat import NewMessage, ChatMessage
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
from use_cases.playlist.save_chat_state_of_playlist import (
    SaveChatStateOfPlaylistUseCase,
)
from utils.fast_api_users_spotify import CurrentActiveUserDep
from chatbot.chatbot import Chatbot
from utils.chatbot_use_cases import ChatbotUseCasesDep

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

_GetPlaylistUseCaseDep = Annotated[
    GetPlaylistUseCase,
    Depends(_init_get_playlist_use_case),
]

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

def _init_save_chat_state_of_playlist_use_case(
        playlist_repo: _PlaylistRepoDep,
):
    return SaveChatStateOfPlaylistUseCase(playlist_repo)

_SaveChatStateOfPlaylistUseCaseDep = Annotated[
    SaveChatStateOfPlaylistUseCase,
    Depends(_init_save_chat_state_of_playlist_use_case),
]

# router

router = APIRouter(
    prefix='/playlists',
    tags=['chat'],
)

@router.get(
    '/{playlist_id}/chat',
    response_model=list[ChatMessage],
)
async def get_chat_of_playlist(
    user: CurrentActiveUserDep,
    get_chat_message_of_playlist_use_case: _GetChatMessagesOfPlaylistUseCaseDep,
    playlist_id: str,
    before: str | None = None,
):
    chat = await get_chat_message_of_playlist_use_case \
        .execute(user, playlist_id, before)

    return [ChatMessage.from_chat_history(m) for m in chat.history]

@router.post('/{playlist_id}/chat', response_model=ChatMessage)
async def send_message(
    user: CurrentActiveUserDep,
    get_playlist_use_case: _GetPlaylistUseCaseDep,
    send_message_use_case: _SendMessageUseCaseDep,
    save_chat_state_of_playlist_use_case: _SaveChatStateOfPlaylistUseCaseDep,
    chat_bot_use_cases: ChatbotUseCasesDep,
    playlist_id: str,
    message: NewMessage,
):
    playlist = await get_playlist_use_case.execute(playlist_id, user)
    chat_bot = Chatbot(playlist, user, chat_bot_use_cases)

    _, response = gather(
        send_message_use_case.execute(playlist, message),
        chat_bot.respond(message.content),
    )

    response_message, _ = await gather(
        send_message_use_case.execute(
            playlist,
            NewMessage(content=response),
            is_bot=True,
        ),
        save_chat_state_of_playlist_use_case.execute(
            playlist,
            chat_bot.export_data(),
        ),
    )

    return ChatMessage.from_chat_history(response_message)
