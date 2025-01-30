from dataclasses import dataclass

from bson import ObjectId

from notebook_gena.mongodb import MongoDB
from notebook_gena.mongoquery import MongoQuery


@dataclass
class UtilityContext:
    name: str
    db_name: str
    tz_name: str
    commodities: list[str]


class UtilityQuery:
    def __init__(self, mongodb: MongoDB):
        self.mongodb = mongodb

    def get_context(self, ut_name: str) -> UtilityContext:
        ut_query = [
            {"$match": {"name": ut_name}},
            {"$project": {"_id": 0, "name": 1, "db_name": "$db", "tz_name": "$timezone", "commodities": 1}},
        ]
        result = self.mongodb.change_db("verdeeco_central_db").mongoQuery().get_first("utility", ut_query)
        return UtilityContext(**result)

    def get_dbname(self, ut_name: str) -> str:
        return self.get_context(ut_name).db_name

    def change_db(self, ut_name: str) -> MongoDB:
        return self.mongodb.change_db(self.get_dbname(ut_name))

    def change_query(self, ut_name: str) -> MongoQuery:
        return self.mongodb.change_db(self.get_dbname(ut_name)).mongoQuery()


class ConsumptionRecordsQuery:
    def __init__(self, posgres_schema: str):
        self.posgres_schema = posgres_schema

    def postgres_max_id_query(self) -> str:
        return f"select max(_id) from {self.posgres_schema}.consumption_records"

    def mongo_paged_query(self, skipValue: int, limitValue: int, start_id: str = None, /) -> str:
        first_id = {} if not start_id else {"_id": {"$gt": ObjectId(start_id)}}

        return [
            {"$match": first_id},
            {"$sort": {"_id": 1}},
            {"$skip": skipValue},
            {"$limit": limitValue},
            {"$unwind": "$consumptions"},
            {
                "$group": {
                    "_id": "$_id",
                    "commodity": {"$first": "$commodity"},
                    "date": {"$first": "$date"},
                    "device": {"$first": "$device"},
                    "flags": {"$first": "$flags"},
                    "minValue": {"$min": "$consumptions.value"},
                    "maxValue": {"$max": "$consumptions.value"},
                    "avgValue": {"$avg": "$consumptions.value"},
                    "theCount": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "commodity": 1,
                    "date": 1,
                    "device": 1,
                    "minValue": {"$toDouble": "$minValue"},
                    "maxValue": {"$toDouble": "$maxValue"},
                    "avgValue": {"$toDouble": "$avgValue"},
                    "theCount": 1,
                    "hasFlag": {"$in": ["ROLLOVER_DETECTED", "$flags"]},
                }
            },
        ]
