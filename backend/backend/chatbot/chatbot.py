from typing import Any
from .utils.protocols.handler import Handler
from .utils.errors import IntentNotFoundError
from .smalltalk.smalltalk_handler import SmalltalkHandler
from .search.search_handler import SearchHandler
from .playlist.playlist_handler import PlaylistHandler
from utils.chatbot_use_cases import ChatbotUseCasesDep
from entities.user import UserEntity
from entities.playlist import PlaylistEntity

class Chatbot():
    def __init__(
        self,
        playlist: PlaylistEntity,
        user: UserEntity,
        use_cases: ChatbotUseCasesDep,
    ):
        self._data = self._init_data(playlist.chat_state)
        self._handlers: dict[str, Handler] = {
            SmalltalkHandler.key: SmalltalkHandler(
                self._data.get(SmalltalkHandler.key),
            ),
            SearchHandler.key: SearchHandler(
                self._data.get(SearchHandler.key),
                user,
                playlist.spotify_playlist_id,
                use_cases,
            ),
            PlaylistHandler.key: PlaylistHandler(
                self._data.get(PlaylistHandler.key)
            ),
        }

    async def respond(self, query: str):
        try:
            if self._previous_key:
                if query == 'CANCEL' or query == 'STOP':
                    self._previous_key = None
                    self._is_finished = True
                    return 'Your request has been cancelled.'

                response, self._is_finished = await self \
                    ._handlers[self._previous_key] \
                    .generate_followup_response(query)
                self._key = self._previous_key
            else:
                self._key, response, self._is_finished = await self \
                    ._process_initial_query(query)

            if self._is_finished and self._key in self._data:
                del self._data[self._key]
            else:
                self._data[self._key] = self._handlers[self._key].export_state()
            self._previous_key = None if self._is_finished else self._key
        except IntentNotFoundError:
            response = "Sorry, I didn't understand that. Can you please rephrase the query?\n"
            response += 'Alternatively, enter "HELP" to learn more about me.'

        return response

    def export_data(self):
        return self._data

    def _init_data(self, data: dict[str, Any]) -> dict[str, Any]:
        return {
            'main': {
                'previous_key': None,
                'key': None,
                'is_finished': True,
            },
        } if not data else data

    async def _process_initial_query(self, query: str) -> tuple[str, str, bool]:
        key = self._find_max_intent_similarity(query)
        if not key:
            raise IntentNotFoundError

        response, is_finished = await self._handlers[key] \
            .generate_initial_response()

        return key, response, is_finished

    def _find_max_intent_similarity(self, query: str):
        results = {
            name: handler.match_intent(query)
            for name, handler in self._handlers.items()
        }

        max_similarity = 0
        max_similarity_key = ''

        for key, similarity in results.items():
            if not similarity:
                continue

            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_key = key

        if not max_similarity:
            return None

        return max_similarity_key

    @property
    def _previous_key(self) -> str | None:
        return self._data['main']['previous_key']

    @_previous_key.setter
    def _previous_key(self, new_key: str | None):
        self._data['main']['previous_key'] = new_key

    @property
    def _key(self):
        return self._data['main']['key']

    @_key.setter
    def _key(self, new_key: str):
        self._data['main']['key'] = new_key

    @property
    def _is_finished(self):
        return self._data['main']['is_finished']

    @_is_finished.setter
    def _is_finished(self, is_finished: bool):
        self._data['main']['is_finished'] = is_finished
