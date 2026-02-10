"""
Database models for the Transcriber application.
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class TranscriptionJob(Base):
    """Model representing a transcription job."""
    __tablename__ = "transcriptionjob"
    
    id = Column(String, primary_key=True)
    filename = Column(String)
    original_path = Column(String)
    status = Column(String)  # queued, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    model = Column(String)  # whisper model name
    language = Column(String, nullable=True)
    speakers_detected = Column(Integer, default=0)
    duration = Column(Float, nullable=True)
    
    # Relationship to segments
    segments = relationship("Segment", back_populates="job", cascade="all, delete-orphan")


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