from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "MaxCopy Backend"
    database_url: str = "postgresql+psycopg2://postgres:421711%40Md@localhost:5432/maxcopy_db"

    class Config:
        env_file = ".env"

settings = Settings()
