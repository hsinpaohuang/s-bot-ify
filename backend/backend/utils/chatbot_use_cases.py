from typing import Annotated
from fastapi import Depends
from repositories.spotify.track_repository import SpotifyTrackRepository
from repositories.spotify.playlist_repository import SpotifyPlaylistRepository
from use_cases.search.search_tracks_use_case import SearchTracksUseCase
from use_cases.playlist.add_tracks_to_playlist import AddTracksToPlaylistUseCase

class ChatbotUseCases():
    search_tracks_use_case = SearchTracksUseCase(SpotifyTrackRepository())
    add_tracks_to_playlist_use_case = AddTracksToPlaylistUseCase(
        SpotifyPlaylistRepository(),
    )

ChatbotUseCasesDep = Annotated[
    ChatbotUseCases,
    Depends(ChatbotUseCases),
]
