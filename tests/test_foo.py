import re

from peek import peek
from sqlalchemy import text

from notebook_gena.foo import foo


def test_foo():
    peek("foo 2")
    assert foo("foo") == "foo"


def test_my_resource(my_resource):
    assert my_resource.get_resources() == ("Resource 1", "Resource 2")


def test_postgres_resource(postgres_container):
    print(postgres_container.get_connection_url())
    # match pattern postgresql+psycopg2://postgres:test_password@localhost:50891/test_database
    pattern = r"^postgresql\+psycopg2:\/\/(?P<username>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)\/(?P<database>[^/]+)$"
    match = re.match(pattern, postgres_container.get_connection_url())
    print(
        f"username:{match.group('username')}; password:{match.group('password')}; host:{match.group('host')}; port:{match.group('port')}; database:{match.group('database')}"
    )
    assert match is not None


def test_mongo_resource(mongo_container):
    print(mongo_container.get_connection_url())
    # validate pattern 'mongodb://test:test@localhost:50155'
    pattern = r"^mongodb:\/\/(?P<username>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)$"
    match = re.match(pattern, mongo_container.get_connection_url())
    print(
        f"username:{match.group('username')}; password:{match.group('password')}; host:{match.group('host')}; port:{match.group('port')}"
    )
    assert match is not None


def test_both_containers(mongo_container, postgres_container):
    assert mongo_container.get_connection_url() is not None
    assert postgres_container.get_connection_url() is not None


def test_postgres_connection(postgres_connection):
    assert postgres_connection is not None
    result = postgres_connection.execute(text("SELECT 1"))
    for row in result:
        assert row[0] == 1
        peek("Connection validated, result:", row[0])
