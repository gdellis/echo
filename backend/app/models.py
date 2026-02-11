"""
Database models for the Transcriber application.
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()


class TranscriptionJob(Base):
    """Model representing a transcription job."""
    __tablename__ = "transcriptionjob"
    
    id = Column(String, primary_key=True)
    filename = Column(String)
    original_path = Column(String)
    # Default values for Python object creation
    status: str
    created_at: datetime
    model: str
    language: str | None
    speakers_detected: int
    duration: float | None
    
    # Database column definitions
    status = Column(String, server_default="queued")
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    completed_at = Column(DateTime, nullable=True)
    model = Column(String, server_default="base")
    language = Column(String, nullable=True)
    speakers_detected = Column(Integer, server_default="0")
    duration = Column(Float, nullable=True)
    
    # Relationship to segments
    segments = relationship("Segment", back_populates="job", cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        """Initialize TranscriptionJob with defaults for unset values."""
        # Set defaults before calling parent init
        if 'status' not in kwargs:
            kwargs['status'] = "queued"
        if 'created_at' not in kwargs:
            kwargs['created_at'] = datetime.now(timezone.utc)
        if 'model' not in kwargs:
            kwargs['model'] = "base"
        if 'language' not in kwargs:
            kwargs['language'] = None
        if 'speakers_detected' not in kwargs:
            kwargs['speakers_detected'] = 0
        if 'duration' not in kwargs:
            kwargs['duration'] = None
        super().__init__(**kwargs)


class Segment(Base):
    """Model representing a transcription segment with speaker label."""
    __tablename__ = "segment"
    
    id = Column(Integer, primary_key=True)
    job_id = Column(String, ForeignKey("transcriptionjob.id"))
    start_time = Column(Float)
    end_time = Column(Float)
    text = Column(String)
    speaker = Column(String)
    confidence = Column(Float)
    
    # Relationship to job
    job = relationship("TranscriptionJob", back_populates="segments")
