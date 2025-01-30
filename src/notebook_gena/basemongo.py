from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


class BaseMongo:
    def __init__(self, _mongoClient: MongoClient, _currentDb: Database):
        self._mongoClient = _mongoClient
        self._currentDb = _currentDb

    @property
    def db_name(self) -> str:
        return self._currentDb.name

    @property
    def db(self) -> Database:
        return self._currentDb

    def collection(self, collection_name: str) -> Collection:
        return self._currentDb.get_collection(collection_name)

    def close(self) -> None:
        self._mongoClient.close()
