from pydantic import BaseModel
from dtos.artist import SpotifyTrackArtist
from dtos.image import SpotifyImages
from dtos.paginated import SpotifyPaginated, Paginated

class SpotifyTrack(BaseModel):
    id: str
    name: str
    album: SpotifyImages
    artists: list[SpotifyTrackArtist]
    uri: str

    @property
    def as_track(self):
        output = self.model_dump(exclude={ 'album', 'artists' })
        output['icon'] = self.album.icon
        output['artists'] = [artist.name for artist in self.artists]

        return Track.model_validate(output)

class SpotifyTrackItem(BaseModel):
    track: SpotifyTrack

class SpotifyTracks(SpotifyPaginated[SpotifyTrackItem], BaseModel):
    @property
    def as_tracks(self):
        output = self.model_dump(include={ 'has_more', 'offset' })
        output['tracks'] = [track.track.as_track for track in self.items]

        return Tracks.model_validate(output)

class SpotifySearchResult(BaseModel):
    tracks: SpotifyPaginated[SpotifyTrack]

    @property
    def as_tracks(self):
        output = self.tracks.model_dump(include={ 'has_more', 'offset' })
        output['tracks'] = [
            spotify_track.as_track
            for spotify_track in self.tracks.items
        ]

        return Tracks.model_validate(output)

class Track(BaseModel):
    id: str
    name: str
    icon: str
    artists: list[str]
    uri: str

class Tracks(Paginated, BaseModel):
    tracks: list[Track]
