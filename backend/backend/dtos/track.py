from typing import Literal
from pydantic import BaseModel
from dtos.image import SpotifyImages
from dtos.paginated import SpotifyPaginated, Paginated

class SpotifyTrack(BaseModel):
    id: str
    name: str
    album: SpotifyImages
    artists: list[dict[Literal['name'], str]]

    @property
    def as_track(self):
        artist_names = [artist['name'] for artist in self.artists]
        if len(artist_names) == 1:
            artists = artist_names[0]
        else:
            artists = f"{', '.join(artist_names[:-1])} and {artist_names[-1]}"

        output = self.model_dump(include={ 'id', 'name' })
        output['icon'] = self.album.icon
        output['artists'] = artists

        return Track.model_validate(output)

class SpotifyTrackItem(BaseModel):
    track: SpotifyTrack

class SpotifyTracks(SpotifyPaginated[SpotifyTrackItem], BaseModel):
    @property
    def as_tracks(self):
        output = self.model_dump(include={ 'has_more', 'offset' })
        output['tracks'] = [track.track.as_track for track in self.items]

        return Tracks.model_validate(output)


class Track(BaseModel):
    id: str
    name: str
    icon: str
    artists: str

class Tracks(Paginated, BaseModel):
    tracks: list[Track]