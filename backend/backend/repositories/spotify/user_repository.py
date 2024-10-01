from entities.user import UserEntity
from dtos.user import SpotifyUser
from utils.spotify import SpotifyAPI

class SpotifyUserRepository():
    async def get_user(
        self,
        user: UserEntity | None = None,
        access_token: str | None = None,
    ):
        if user:
            spotify_api = SpotifyAPI(user)
        elif access_token:
            spotify_api = SpotifyAPI(access_token=access_token)
        else:
            raise ValueError('Invalid input_data')

        return await spotify_api.get('/v1/me', SpotifyUser)
