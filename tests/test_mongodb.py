import pytest
from peek import peek
from pymongo.collection import Collection
from pymongo.database import Database

from notebook_gena.mongodb import MongoDB, MongoDBException
from notebook_gena.mongoquery import MongoQuery


def test_mongodb_connect_with_url(mongo_container):
    # Test connecting with direct MongoDB URL
    mongo_url = mongo_container.get_connection_url() + "/test_db"
    peek(mongo_url)
    mongodb = MongoDB.connect(mongo_url)
    assert isinstance(mongodb, MongoDB)
    assert isinstance(mongodb.db, Database)
    assert mongodb.db_name == "test_db"


def test_mongodb_connect_without_db_name(mongo_container):
    # Test connecting with direct MongoDB URL
    mongo_url = mongo_container.get_connection_url()
    peek(mongo_url)
    with pytest.raises(MongoDBException) as ex:
        mongodb = MongoDB.connect(mongo_url)
        print(mongodb)
    assert str(ex.value) == f"Missing default database name in connection url:{mongo_url}"


# @pytest.mark.skip(reason="This test is not working as expected")
def test_mongodb_connect_with_url_and_name(mongo_container):
    # Test connecting with direct MongoDB URL
    mongo_url = mongo_container.get_connection_url()
    peek(mongo_url)
    mongodb = MongoDB.connect_with_db_name(mongo_url, "test_db")
    assert isinstance(mongodb, MongoDB)
    assert isinstance(mongodb.db, Database)
    assert mongodb.db_name == "test_db"


def test_mongodb_change_db(mongo_container):
    # Test connecting with direct MongoDB URL
    mongo_url = mongo_container.get_connection_url() + "/test_db"
    peek(mongo_url)
    mongodb = MongoDB.connect(mongo_url)
    assert isinstance(mongodb, MongoDB)
    assert isinstance(mongodb.db, Database)
    assert mongodb.db_name == "test_db"

    mongodb_2 = mongodb.change_db("test_db_2")
    assert isinstance(mongodb_2, MongoDB)
    assert isinstance(mongodb_2.db, Database)
    assert mongodb_2.db_name == "test_db_2"

    peek(mongodb_2.list_database_names())


def test_mongodb_collection(mongo_container):
    # Test connecting with direct MongoDB URL
    mongodb = MongoDB.connect_with_db_name(mongo_container.get_connection_url(), "test_db")
    collection = mongodb.collection("test_collection")
    assert isinstance(collection, Collection)
    assert collection.name == "test_collection"
    peek(mongodb.list_collection_names())


def test_list_database_names(mongo_container):
    mongodb = MongoDB.connect_with_db_name(mongo_container.get_connection_url(), "test_db")
    mongodb.collection("test_collection").insert_one({"test": "data"})

    mongodb_2 = mongodb.change_db("test_db_2")
    mongodb_2.collection("test_collection_2").insert_one({"test": "data"})

    assert {"test_db", "test_db_2"}.issubset(set(mongodb.list_database_names()))


def test_list_collection_names(mongo_container):
    mongodb = MongoDB.connect_with_db_name(mongo_container.get_connection_url(), "test_db")
    mongodb.collection("test_collection").insert_one({"test": "data"})

    mongodb_2 = mongodb.change_db("test_db_2")
    mongodb_2.collection("test_collection_2").insert_one({"test": "data"})

    assert {"test_collection"}.issubset(set(mongodb.list_collection_names()))
    assert {"test_collection_2"}.issubset(set(mongodb_2.list_collection_names()))


def test_mongoquery(mongo_container):
    mongodb = MongoDB.connect_with_db_name(mongo_container.get_connection_url(), "test_db")
    mongoquery = mongodb.mongoQuery()
    assert isinstance(mongoquery, MongoQuery)
