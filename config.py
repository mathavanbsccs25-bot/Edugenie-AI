import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "EduGenie"
    APP_VERSION = "1.0.0"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"


settings = Settings()
