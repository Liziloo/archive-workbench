import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Manually find the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    # Pydantic will look for these in the environment
    DATABASE_URL: str
    STAGING_DIRECTORY: str
    PROJECT_NAME: str = "Archive Workbench"

    # This is the "magic" that connects the .env to the class
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
    # If you are seeing this in VS Code as a red squiggly,
    # it's often a linter error. Run the script to be sure.