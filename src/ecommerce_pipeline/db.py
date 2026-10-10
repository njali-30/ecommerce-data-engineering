
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from ecommerce_pipeline.config import get_database_url


def create_db_engine() -> Engine:
    """Create a SQLAlchemy engine for PostgreSQL."""
    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
    )


def test_connection() -> str:
    """Verify the database connection and return the database name."""
    engine = create_db_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT current_database()")
            )
            return result.scalar_one()
    finally:
        engine.dispose()
