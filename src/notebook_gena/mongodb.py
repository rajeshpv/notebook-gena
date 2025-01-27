import os

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


class MongoDBException(Exception):
    pass


class MongoDB:
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

    @staticmethod
    def connect(env_name_or_url: str) -> "MongoDB":
        mongo_con_url = (
            env_name_or_url
            if env_name_or_url.startswith("mongodb")
            else os.getenv(env_name_or_url, f"unknown env_name:{env_name_or_url}")
        )
        client: MongoClient = MongoClient(mongo_con_url, authSource="admin")
        if client._default_database_name is None:
            raise MongoDBException(f"Missing default database name in connection url:{mongo_con_url}")
        return MongoDB(client, client.get_database())

    @staticmethod
    def connect_with_db_name(env_name_or_url: str, db_name: str, /) -> "MongoDB":
        mongo_con_url = (
            env_name_or_url
            if env_name_or_url.startswith("mongodb")
            else os.getenv(env_name_or_url, f"unknown env_name:{env_name_or_url}")
        )
        client: MongoClient = MongoClient(mongo_con_url, authSource="admin")
        return MongoDB(client, client.get_database(db_name))

    def change_db(self, db_name: str) -> "MongoDB":
        new_client: MongoClient = self._mongoClient

        return MongoDB(new_client, new_client.get_database(db_name))

    def list_database_names(self) -> list[str]:
        return self._mongoClient.list_database_names()

    def list_collection_names(self) -> list[str]:
        return self._currentDb.list_collection_names()
