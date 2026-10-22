from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class Settings(BaseSettings):
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

def test_connection() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print(f"Database connection successful: {result.scalar()}")