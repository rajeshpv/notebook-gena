from pymongo.command_cursor import CommandCursor

from notebook_gena.mongodb import MongoDB
from notebook_gena.mongoquery import MongoQuery


def test_get_cursor(mongo_container):
    mongoQuery = MongoDB.connect(mongo_container.get_connection_url() + "/test_db").mongoQuery()
    assert isinstance(mongoQuery, MongoQuery)
    cursor = mongoQuery.get_cursor("test_collection_mongoquery")
    assert isinstance(cursor, CommandCursor)
    assert cursor.to_list(1) == []

    single_record = {"test": "data"}
    mongoQuery.collection("test_collection_mongoquery").insert_one(single_record)
    cursor = mongoQuery.get_cursor("test_collection_mongoquery")
    fetch_record = cursor.to_list(1)[0]
    assert fetch_record == single_record


def test_get_first(mongo_container):
    mongoQuery = MongoDB.connect(mongo_container.get_connection_url() + "/test_db").mongoQuery()
    records = [{"_id": 0}, {"_id": 1}]
    mongoQuery.collection("col_get_first").insert_many(records)
    fetch_record = mongoQuery.get_first("col_get_first")
    assert fetch_record == records[0]


def test_get_listall(mongo_container):
    mongoQuery = MongoDB.connect(mongo_container.get_connection_url() + "/test_db").mongoQuery()
    records1 = [{"_id": 0}, {"_id": 1}]
    mongoQuery.collection("col_get_list").insert_many(records1)
    fetch_records = mongoQuery.get_listall("col_get_list")
    assert fetch_records == records1

    # second set of records
    records2 = [{"_id": 2}, {"_id": 3}]
    mongoQuery.collection("col_get_list").insert_many(records2)
    fetch_records2 = mongoQuery.get_listall("col_get_list")
    assert fetch_records2 == records1 + records2


def test_get_count(mongo_container):
    mongoQuery = MongoDB.connect(mongo_container.get_connection_url() + "/test_db").mongoQuery()
    records = [{"_id": i} for i in range(10)]
    mongoQuery.collection("col_get_count").insert_many(records)
    count = mongoQuery.get_count("col_get_count")
    assert count == 10


def test_get_page(mongo_container):
    mongoQuery = MongoDB.connect(mongo_container.get_connection_url() + "/test_db").mongoQuery()
    records = [{"_id": i} for i in range(12)]
    mongoQuery.collection("col_get_page").insert_many(records)
    page = mongoQuery.get_page("col_get_page", [], 0, 5)
    assert page == records[0:5]

    page = mongoQuery.get_page("col_get_page", [], 5, 5)
    assert page == records[5:10]

    page = mongoQuery.get_page("col_get_page", [], 10, 5)
    assert page == records[10:12]

    page = mongoQuery.get_page("col_get_page", [])
    assert page == records[0:12]
