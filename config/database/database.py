from dotenv import dotenv_values
from motor.motor_asyncio import AsyncIOMotorClient
from typing import AsyncGenerator
from logging import info
from contextlib import asynccontextmanager


# Cargar configuración desde el archivo .env
config = dotenv_values(".env")


async def get_db_connection() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client = AsyncIOMotorClient(config["MONGO_URI"])
    db = client[config["DB_NAME"]]
    try:
        yield db
    finally:
        client.close()
