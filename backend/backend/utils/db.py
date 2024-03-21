from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from utils.env import settings

from entities.user import UserEntity
from entities.playlist import PlaylistEntity

async def connect_to_db():
    username = settings.db_root_username
    password = settings.db_root_password
    mode = settings.fast_api_mode

    client = AsyncIOMotorClient(
        f'mongodb://{username}:{password}@host.docker.internal:27071',
    )

    await init_beanie(database=client[f's-bot-ify_{mode}'], document_models=[
        UserEntity,
        PlaylistEntity,
    ])
