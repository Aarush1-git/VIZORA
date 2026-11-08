from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "VIZORA API"
    debug: bool = False
    database_url: str

    secret_key: str
    access_token_expire_minutes: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    


settings = Settings()