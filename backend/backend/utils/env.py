from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class _Settings(BaseSettings):
    model_config = SettingsConfigDict(secrets_dir='/run/secrets')

    fast_api_mode: Literal['DEV', 'PROD']

    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_url: str
    spotify_jwt_secret: str
    spotify_oauth_state: str

    db_root_username: str
    db_root_password: str

    frontend_entry_point: str

settings = _Settings() # pyright:ignore
