"""
File operations utilities for the Transcriber backend.
"""
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


def get_database_engine():
    """Get database engine."""
    return create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    """Get database session."""
    engine = get_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def generate_job_id() -> str:
    """Generate a unique job ID."""
    return str(uuid.uuid4())


def save_uploaded_file(file_path: str, upload_dir: Optional[str] = None) -> str:
    """
    Save an uploaded file to the upload directory.
    
    Args:
        file_path: Path to the uploaded file
        upload_dir: Custom upload directory (optional)
    
    Returns:
        str: Path to the saved file
    """
    upload_dir = upload_dir or settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    
    filename = os.path.basename(file_path)
    dest_path = os.path.join(upload_dir, filename)
    
    # Move file to upload directory
    if os.path.exists(file_path):
        shutil.move(file_path, dest_path)
    
    return dest_path


def get_file_extension(filename: str) -> str:
    """Get file extension in lowercase."""
    return os.path.splitext(filename)[1].lower().lstrip(".")


def is_valid_audio_format(filename: str) -> bool:
    """Check if the file has a valid audio format."""
    valid_extensions = {"mp3", "wav", "mp4", "mov", "m4a", "flac"}
    ext = get_file_extension(filename)
    return ext in valid_extensions


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(file_path)


def format_duration(seconds: float) -> str:
    """Format duration in seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def cleanup_temp_files(file_path: str):
    """Clean up temporary files."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")