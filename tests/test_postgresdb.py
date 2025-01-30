import re

from peek import peek
from sqlalchemy import create_engine, text

from notebook_gena.postgresdb import PostgresDB


def test_parse_url(postgres_container):
    db_url = postgres_container.get_connection_url()

    pattern = r"^postgresql\+psycopg2:\/\/(?P<username>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)\/(?P<database>[^/]+)$"
    match = re.match(pattern, db_url)
    assert match is not None
    assert match.group("username") == "postgres"
    assert match.group("password") == "test_password"
    assert match.group("database") == "test_database"


def create_table(db_url: str, ddl_query: str):
    engine = create_engine(db_url, echo=True).execution_options(isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        # conn.execute(text(f"CREATE DATABASE if not exists test_database"))
        conn.execute(text(ddl_query))
        conn.commit()


def test_select_scalar_None(postgres_container):
    db_url = postgres_container.get_connection_url()
    peek(db_url)

    ddl_query = """CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR,
        age INT
      )"""

    create_table(db_url, ddl_query)

    pgdb = PostgresDB(postgres_container.get_connection_url())
    scalar = pgdb.select_scalar("SELECT max(age) FROM users")
    peek(scalar)
    assert scalar is None


def test_insert_one(postgres_container):
    db_url = postgres_container.get_connection_url()

    pgdb = PostgresDB(db_url)
    insert_count = pgdb.insert("INSERT INTO users (name, age) VALUES (:name, :age)", {"name": "name21", "age": 21})
    peek(insert_count)
    assert insert_count == 1


def test_select_one(postgres_container):
    pgdb = PostgresDB(postgres_container.get_connection_url())
    row = pgdb.select_one("SELECT * FROM users WHERE name = :name", {"name": "name21"})
    assert row is not None
    assert row["name"] == "name21"
    assert row["age"] == 21


def test_select_all(postgres_container):
    pgdb = PostgresDB(postgres_container.get_connection_url())
    rows = pgdb.select_all("SELECT * FROM users")
    assert len(rows) == 1
    assert rows[0]["name"] == "name21"
    assert rows[0]["age"] == 21


def test_select_scalar_with_value(postgres_container):
    pgdb = PostgresDB(postgres_container.get_connection_url())
    scalar = pgdb.select_scalar("SELECT COUNT(*) FROM users")
    peek(scalar)
    assert scalar == 1


def test_update(postgres_container):
    pgdb = PostgresDB(postgres_container.get_connection_url())
    update_count = pgdb.update("UPDATE users SET age = :age WHERE name = :name", {"name": "name21", "age": 22})
    peek(update_count)
    assert update_count == 1

    row = pgdb.select_one("SELECT * FROM users WHERE name = :name", {"name": "name21"})
    assert row is not None
    assert row["name"] == "name21"
    assert row["age"] == 22


def test_delete(postgres_container):
    pgdb = PostgresDB(postgres_container.get_connection_url())
    delete_count = pgdb.delete("DELETE FROM users WHERE name = :name", {"name": "name21"})
    peek(delete_count)
    assert delete_count == 1


def test_execute_ddl(postgres_container):
    pgdb = PostgresDB(postgres_container.get_connection_url())
    ddl_query = "CREATE TABLE users_2(id SERIAL PRIMARY KEY, name VARCHAR, age INT)"
    execute_ddl_count = pgdb.execute_ddl(ddl_query)
    peek(execute_ddl_count)
    assert execute_ddl_count is True

    insert_count = pgdb.insert("INSERT INTO users_2 (name, age) VALUES (:name, :age)", {"name": "name21", "age": 21})
    peek(insert_count)
    assert insert_count == 1
