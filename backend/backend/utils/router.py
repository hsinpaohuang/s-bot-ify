from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from utils.env import settings

from routes.spotify_auth import spotify_oauth_router
from routes.user_info import router as user_info_router

_routers = [user_info_router]

def setup_routers(app: FastAPI):
    setup_oauth_routers(app)

    for router in _routers:
        app.include_router(router, prefix='/api')

    if settings.fast_api_mode == 'PROD':
        app.mount('/{full_path:path}', StaticFiles(directory='static'), name='static')
        pass
    elif settings.fast_api_mode == 'DEV':
        @app.get('/{full_path:path}', response_class=RedirectResponse)
        def redirect_to_frontend(full_path: str): #pyright: ignore
            return f'{settings.frontend_entry_point}/{full_path}'

def setup_oauth_routers(app: FastAPI):
    app.include_router(
        spotify_oauth_router,
        prefix='/auth/spotify',
        tags=['auth'],
    )
