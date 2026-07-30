import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    DATABASE_URL: str
    STAGING_DIRECTORY: str

    REDIS_URL: str
    OLLAMA_HOST: str = "http://localhost:11434"

    PATH_RAW: str
    PATH_EDITED: str
    PATH_CARL: str

    PROJECT_NAME: str = "Archive Workbench"
    model_config = SettingsConfigDict(
        env_file=dotenv_path,
        env_file_encoding='utf-8',
        extra="ignore"
    )

# Instantiate settings
try:
    settings = Settings()
    if __name__ == "__main__":
        print(f"✅ .env found at: {dotenv_path}")
        print(f"✅ Settings loaded successfully.")
        print(f"📡 Target DB: {settings.DATABASE_URL.split('@')[-1]}")
except Exception as e:
    print(f"❌ Settings Error: {e}")