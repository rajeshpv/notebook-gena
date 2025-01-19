import warnings

import pytest
from my_resource import MyResource
from sqlalchemy import Connection, create_engine
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.mongodb import MongoDbContainer
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def my_resource():
    with MyResource() as res:
        yield res
    print("conftest.py:Cleaning up resources...")


@pytest.fixture(scope="session")
def postgres_container() -> PostgresContainer:
    """
    Setup postgres container; note port is not specified, so it will be random,
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="S106")
        warnings.filterwarnings("ignore", message="S105")
        CONST_PWD = "test_pwd"
        postgres = PostgresContainer(
            image="postgres:14",
            username="postgres",
            password=CONST_PWD,
            dbname="test_database",
        )
        with postgres:
            wait_for_logs(
                postgres,
                r"UTC \[1\] LOG:  database system is ready to accept connections",
                10,
            )
            yield postgres


@pytest.fixture(scope="session")
def mongo_container() -> MongoDbContainer:
    """
    Setup mongo container; note port is not specified, so it will be random,
    """
    mongo = MongoDbContainer(
        image="mongo:6.0.7",
    )
    with mongo:
        wait_for_logs(
            mongo,
            r"Waiting for connections",
            10,
        )
        yield mongo


@pytest.fixture(scope="session")
def postgres_connection(postgres_container) -> Connection:
    """
    Setup postgres engine; note port is not specified, so it will be random,
    """
    engine = create_engine(postgres_container.get_connection_url(), pool_pre_ping=True)
    with engine.connect() as connection:
        yield connection
