import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_name: str
    selected_database: str
    ex_service_check_action_url: str

    class Config:
        env_file = rf"{pathlib.Path(__file__).resolve().parent.parent}/.env"
        print(env_file)


settings = Settings()
