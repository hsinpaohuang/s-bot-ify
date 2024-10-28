from os import path
import pickle
import pandas as pd
from typing import cast, Any
from enum import Enum
from ..confirmation.confirmation_classifier import confirmation_classifier
from ..utils.corpus_processor import CorpusProcessor
from ..utils.protocols.handler import Handler
from ..utils.find_max_similarity import find_max_similarity
from ..utils.aggregate import aggregate
from ..utils.errors import IntentNotFoundError
import numpy.typing as npt
import numpy as np
from utils.chatbot_use_cases import ChatbotUseCases
from entities.user import UserEntity
from dtos.track import Tracks

class _FollowupType(str, Enum):
    RemoveFromPlaylist = 'RemoveFromPlaylist'
    RemoveAll = 'RemoveAll'

class _IntentType(str, Enum):
    PrevPage = 'PrevPage'
    NextPage = 'NextPage'
    First = 'First'
    Second = 'Second'
    Third = 'Third'
    Fourth = 'Fourth'
    Fifth = 'Fifth'

class PlaylistHandler(Handler):
    key = 'playlist'
    _min_similarity = 0.65
    _min_no_confirmation_similarity = 0.8

    _non_initial_intents = [
        _IntentType.PrevPage,
        _IntentType.NextPage,
        _IntentType.First,
        _IntentType.Second,
        _IntentType.Third,
        _IntentType.Fourth,
        _IntentType.Fifth,
    ]

    def __init__(
        self,
        state: dict[str, Any] | None,
        user: UserEntity,
        spotify_playlist_id: str,
        use_cases: ChatbotUseCases,
    ):
        self._base_path = path.dirname(__file__)
        self._dataset, self._processor, self._doc_term_matrix = self._load_model()
        self._state = state or {}
        self._user = user
        self._spotify_playlist_id = spotify_playlist_id
        self._use_cases = use_cases

    def match_intent(self, query: str, initial: bool = True):
        transformed = self._processor.transform(query)
        flattened = cast(npt.NDArray[np.float64], transformed.toarray().flatten()) # pyright: ignore
        if np.sum(flattened) == 0:
            # none of the tokens in query is in the vocab, so no entry can be matched
            return None

        index, similarity = find_max_similarity(self._doc_term_matrix, flattened)

        # if similarity is smaller than the arbitrary threshold,
        # then the similarity is too low to be considered valid
        if similarity < self._min_similarity:
            return None

        entry = self._dataset.iloc[index]
        intent_type = cast(str, entry['FollowupType'])
        if initial and intent_type in self._non_initial_intents:
            # These queries aren't meant to be an initial query
            return None

        self._state['index'] = index
        self._state['similarity'] = similarity

        return similarity

    async def generate_initial_response(self):
        similarity = cast(float, self._state['similarity'])
        index = cast(int, self._state['index'])

        if similarity >= self._min_no_confirmation_similarity:
            return await self._get_initial_response()
        elif similarity >= self._min_similarity:
            self._state['index'] = index
            self._state['from_confirmation'] = True
            question = self._dataset.iloc[index]['Question']
            response = f"I'm sorry, I didn't quite understand that. Did you mean \"{question}\"?"
            return response, False

        raise IntentNotFoundError

    async def generate_followup_response(self, query: str):
        if self._state.get('from_confirmation'):
            if confirmation_classifier.predict(query):
                response, is_finished = await self._get_initial_response()
            else:
                response = "My apologies for misunderstanding your query. Can you please rephrase it?"
                is_finished = True

            del self._state['index'], self._state['similarity'], self._state['from_confirmation']
        else:
            response, is_finished = await self._get_followup_response(query)

        return response, is_finished

    async def _get_initial_response(self):
        index = cast(int, self._state['index'])
        entry = self._dataset.iloc[index]
        followup_type = cast(str, entry['FollowupType'])
        self._state['followup_type'] = followup_type

        match followup_type:
            case _FollowupType.RemoveFromPlaylist:
                self._state['page'] = 1
                response, is_finished = await self._realise_playlist()
            case _FollowupType.RemoveAll:
                if True: # todo: if playlist length is 0
                    response = 'Your playlist is empty!'
                    is_finished = True
                else:
                    response = 'Do you really want to remove all songs from your playlist?'
                    is_finished = False
            case _:
                response = cast(str, entry['Response'])
                is_finished = False

        return response, is_finished

    async def _get_followup_response(self, query: str):
        match self._state.get('followup_type'):
            case _FollowupType.RemoveFromPlaylist:
                    return self._handle_remove_from_playlist(query)
            case _FollowupType.RemoveAll:
                if not confirmation_classifier.predict(query):
                    return "Ok. I won't delete your playlist.", True

                song_count = self._realise_song_count()
                # todo: clear playlist


                index = cast(int, self._state['index'])
                entry = self._dataset.iloc[index]

                response = cast(str, entry['Response']).format(song_count=song_count)

                return response, True
            case _:
                pass

        intent = self.match_intent(query, False)
        if intent == None:
            raise IntentNotFoundError

        index = cast(int, self._state['index']) # index is set by match_intent
        entry = self._dataset.iloc[index]
        page = cast(int, self._state['page'])

        match entry['FollowupType']:
            case _IntentType.PrevPage:
                if page == 1:
                    return 'You are already at the first page', False

                self._state['page'] = page - 1
                return await self._realise_playlist()
            case _IntentType.NextPage:
                self._state['page'] = page + 1
                return await self._realise_playlist()
            case _:
                raise IntentNotFoundError

    def export_state(self):
        return self._state

    def _load_model(self):
        model_path = path.join(self._base_path, 'playlist_model.pickle')

        if path.isfile(model_path):
            with open(model_path, 'rb') as f:
                model = cast(
                    tuple[pd.DataFrame, CorpusProcessor, npt.NDArray[np.float64]],
                    pickle.load(f),
                )
        else:
            model = self._initialise_model()
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)

        return model

    def _initialise_model(self):
        dataset = pd.read_csv(path.join(self._base_path, 'playlist_dataset.csv'))
        processor = CorpusProcessor()
        questions = cast(npt.NDArray[np.str_], dataset['Question'].values)
        doc_term_matrix = processor.fit_transform(questions)

        return dataset, processor, doc_term_matrix

    async def _realise_playlist(self) -> tuple[str, bool]:
        page = cast(int, self._state.get('page', 1))
        start = (page - 1) * 5
        playlist = await self \
            ._use_cases\
            .get_spotify_tracks_of_playlist_use_case \
            .execute(self._user, self._spotify_playlist_id, start)
        self._state['tracks'] = playlist.model_dump()

        if len(playlist.tracks) == 0:
            if page == 1:
                return "Your playlist is empty! Let's start by searching for a song to add to it!", True
            else:
                return "That's the end of your playlist.", False

        response = f'Here is page {page} of your playlist: \n'

        for index, song in enumerate(playlist.tracks):
            artists = self._aggregate_artists(song.artists)
            response += f'{index + 1}.\n{song.name} by {artists}\n\n'
            # todo: song url

        if len(playlist.tracks) < 5:
            response += "You've reached the end of your playlist.\n"
            if page != 1:
                response += 'You can navigate your playlist with "previous page"\n'
        else:
            if page != 1:
                response += 'You can navigate your playlist with "next page" or "previous page"\n'
            else:
                response += 'You can navigate your playlist with "next page"\n'

        if self._state.get('followup_type') == _FollowupType.RemoveFromPlaylist:
            response += '\nWhich one would you like to remove from your playlist? (1 ~ 5)'

        return response, False

    def _aggregate_artists(self, artists: list[str]):
        return '' if len(artists) == 0 else aggregate(artists)

    def _handle_remove_from_playlist(self, query: str):
        if query in ['1', '2', '3', '4', '5']:
            selected = int(query)
        else:
            similarity = self.match_intent(query, False)
            if similarity == None:
                raise IntentNotFoundError

            index = cast(int, self._state['index'])
            entry = self._dataset.iloc[index]
            intent_type = cast(str, entry['FollowupType'])

            match intent_type:
                case _IntentType.First:
                    selected = 1
                case _IntentType.Second:
                    selected = 2
                case _IntentType.Third:
                    selected = 3
                case _IntentType.Fourth:
                    selected = 4
                case _IntentType.Fifth:
                    selected = 5
                case _:
                    raise IntentNotFoundError

        tracks = Tracks.model_validate(self._state['tracks'])
        song = tracks.tracks[selected - 1]

        artists = self._aggregate_artists(song.artists)
        response = f'Done! {song.name} by {artists} has been removed from your playlist.'

        return response, True

    def _realise_song_count(self):
        song_count = 0 # todo: song_count = playlist length

        if song_count > 1:
            output = f'All {song_count} songs'
        else:
            output = '1 song'

        return output
