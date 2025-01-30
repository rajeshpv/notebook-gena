from typing import Any

from peek import peek
from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor
from pymongo.database import Database

from notebook_gena.mongodb import BaseMongo


class MongoQuery(BaseMongo):
    def __init__(self, _mongoClient: MongoClient, _currentDb: Database):
        super().__init__(_mongoClient, _currentDb)

    def change_db(self, db_name: str) -> "MongoQuery":
        new_client: MongoClient = self._mongoClient
        return MongoQuery(new_client, new_client.get_database(db_name))

    def get_cursor(self, collection_name: str, pipeline: list = []) -> CommandCursor:
        return self._currentDb.get_collection(collection_name).aggregate(pipeline, allowDiskUse=True)

    def get_first(self, col_name: str, pipeline: list = []) -> Any:
        found = None
        result_list = self.get_cursor(col_name, [*pipeline, {"$limit": 1}]).to_list(1)
        if len(result_list) > 0:
            found = result_list[0]
        return found

    def get_listall(self, col_name: str, pipeline: list = [], limit: int | None = None) -> list[Any]:
        return self.get_cursor(col_name, pipeline).to_list(limit)

    def get_count(self, col_name: str, pipeline: list = []) -> int:
        append = {"$group": {"_id": None, "totalItems": {"$sum": 1}}}
        first_result = self.get_listall(col_name, [*pipeline, append])[0]
        peek(first_result)
        return int(first_result["totalItems"])

    def get_page(
        self, col_name: str, pipeline: list = [], first_item_index: int = 0, items_per_page: int = 20
    ) -> list[Any]:
        return self.get_listall(col_name, [*pipeline, {"$skip": first_item_index}, {"$limit": items_per_page}])
