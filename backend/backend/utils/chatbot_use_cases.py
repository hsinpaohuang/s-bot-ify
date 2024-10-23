from typing import Annotated
from fastapi import Depends
from repositories.spotify.track_repository import SpotifyTrackRepository
from use_cases.search.search_tracks_use_case import SearchTracksUseCase

class ChatbotUseCases():
    search_tracks_use_case = SearchTracksUseCase(SpotifyTrackRepository())

ChatbotUseCasesDep = Annotated[
    ChatbotUseCases,
    Depends(ChatbotUseCases),
]
