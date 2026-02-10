"""
Backend configuration settings for the Transcriber application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # FastAPI
    APP_NAME: str = os.getenv("APP_NAME", "Echo API")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # Whisper
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")
    WHISPER_DEVICE: str = os.getenv("WHISPER_DEVICE", "cpu")
    
    # pyannote.audio
    PYANNOTE_MODEL: str = os.getenv("PYANNOTE_MODEL", "pyannote/speaker-diarization")
    
    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # File Upload
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "524288000"))  # 500MB
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/tmp/transcriber")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./transcriber.db")
    
    # Video frames for preview
    PREVIEW_FRAMES: int = 5

settings = Settings()