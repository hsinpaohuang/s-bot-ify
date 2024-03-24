from utils.env import settings
from utils.fast_api_users_spotify import (
    fastapi_users,
    oauth_client,
    auth_backend,
)

spotify_oauth_router = fastapi_users.get_oauth_router(
    oauth_client,
    auth_backend,
    settings.spotify_oauth_state,
    redirect_url=settings.spotify_redirect_url,
    is_verified_by_default=True,
)
