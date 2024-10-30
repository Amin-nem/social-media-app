from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    DATABASE_HOSTNAME : str
    DATABASE_PASSWORD : str
    DATABASE_USERNAME : str
    DATABASE_NAME : str
    DATABASE_PORT : str

    class Config:
        env_file = ".env"


settings = Settings()