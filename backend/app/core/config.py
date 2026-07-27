import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    # We use Field(..., validation_alias=...) to ensure it maps correctly
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    STAGING_DIRECTORY: str = Field(..., validation_alias="STAGING_DIRECTORY")

    PROJECT_NAME: str = "Archive Workbench"

    # This tells Pydantic to look at the .env file found by find_dotenv
    model_config = SettingsConfigDict(
        env_file=dotenv_path,
        env_file_encoding='utf-8',
        extra="ignore"
    )

# --- DEBUG PRINT ---
# This will help us confirm the file is found and the variables are loaded
if not dotenv_path:
    print("❌ ERROR: .env file not found by find_dotenv()")
else:
    print(f"✅ Found .env at: {dotenv_path}")

try:
    settings = Settings()
    print("✅ Settings loaded successfully.")
except Exception as e:
    print(f"❌ Settings Validation Error: {e}")
    # We raise here to stop the app before it fails deeper in the stack
    raise e