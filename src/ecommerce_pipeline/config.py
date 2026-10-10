
import os

from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    """Build the PostgreSQL connection URL from environment variables."""
    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing_variables = [
        name for name in required_variables if not os.getenv(name)
    ]

    if missing_variables:
        raise ValueError(
            "Missing database environment variables: "
            + ", ".join(missing_variables)
        )

    from sqlalchemy.engine import URL

    return URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )
