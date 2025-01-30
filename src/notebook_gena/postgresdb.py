from typing import Any

from sqlalchemy import create_engine, text


class PostgresDB:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url).execution_options(isolation_level="AUTOCOMMIT")

    def insert(self, query: str, params: list[dict[str, Any]] | dict[str, Any] | Any = None) -> int:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params).rowcount
            return result

    def select_one(self, query: str, params: dict[str, Any] | Any = None) -> dict[str, Any] | None:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            row = result.fetchone()
            return dict(zip(result.keys(), row)) if row else None

    def select_all(self, query: str, params: dict[str, Any] | Any = None) -> list[dict[str, Any]]:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            rows = result.fetchall()
            return [dict(zip(result.keys(), row)) for row in rows]

    def select_scalar(self, query: str, params: dict[str, Any] | Any = None) -> Any | None:
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params)
            return result.scalar()

    def execute_ddl(self, query: str, params: dict[str, Any] | Any = None) -> bool:
        with self.engine.connect() as conn:
            conn.execute(text(query), params)
            conn.commit()
            return True

    def update(self, query: str, params: dict[str, Any] | Any = None) -> int:
        return self.insert(query, params)

    def delete(self, query: str, params: dict[str, Any] | Any = None) -> int:
        return self.insert(query, params)
