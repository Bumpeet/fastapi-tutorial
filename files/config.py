from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_password: str
    db_username: str
    db_name: str
    db_hostname: str
    db_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}"
