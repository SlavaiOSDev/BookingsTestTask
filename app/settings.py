import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    @property
    def database_url(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings(
    db_host=os.getenv("DB_HOST", "localhost"),
    db_port=int(os.getenv("DB_PORT", "5432")),
    db_name=os.getenv("DB_NAME", "fastapi_db"),
    db_user=os.getenv("DB_USER", "postgres"),
    db_password=os.getenv("DB_PASSWORD", "secret123"),
)
