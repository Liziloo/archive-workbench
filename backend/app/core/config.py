import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Manually find the .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    DATABASE_URL: str
    STAGING_DIRECTORY: str

    # Add the three specific source paths
    PATH_RAW: str
    PATH_EDITED: str
    PATH_CARL: str

    PROJECT_NAME: str = "Archive Workbench"
    model_config = SettingsConfigDict(env_file=dotenv_path, extra="ignore")

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