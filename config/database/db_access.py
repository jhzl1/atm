from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


class Database:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db

    @property
    def users(self) -> AsyncIOMotorCollection:
        return self._db["users"]


def get_database(db: AsyncIOMotorDatabase) -> Database:
    return Database(db)
