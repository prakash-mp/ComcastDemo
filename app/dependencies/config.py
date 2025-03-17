from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_SERVER: str
    DB_PORT: int
    DB_NAME: str
    LOG_LEVEL: str
    LOGGER_APP_NAME: str
    LOGGER_FORMAT = "[%(asctime)s] [%(levelname)s] [{}] [{}] [%(filename)s -> %(funcName)s()] [%(lineno)s] %(message)s"
    LOGGER_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


settings = Settings()
