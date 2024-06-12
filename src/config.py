from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TOKEN: str

    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_NAME: str
    MONGODB_COLLECTION_NAME: str

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
