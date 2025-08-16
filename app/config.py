from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./gmv_fleet.db"
    JWT_SECRET: str = "sua_chave_secreta_muito_segura_aqui_2024"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Carregar configurações do ambiente ou usar valores padrão
settings = Settings()