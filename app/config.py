import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_name: str

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent}/.env"
