import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./personalone.db")
DB_SCHEMA = os.getenv("DB_SCHEMA", "").strip() or None
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    metadata = MetaData(schema=DB_SCHEMA)


def create_database_schema():
    if DB_SCHEMA and engine.dialect.name == "postgresql":
        schema_name = engine.dialect.identifier_preparer.quote(DB_SCHEMA)
        with engine.begin() as connection:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
