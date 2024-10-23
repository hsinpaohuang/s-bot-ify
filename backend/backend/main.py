from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.db import connect_to_db
from utils.router import setup_routers
from utils.env import settings
from chatbot.utils.check_nltk_data import check_nltk_data

check_nltk_data()

@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_db()
    yield

cors_origins: list[str] = []

if (settings.fast_api_mode == 'DEV'):
    cors_origins.append(settings.frontend_entry_point)

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods='*',
    allow_headers='*',
)
setup_routers(app)
