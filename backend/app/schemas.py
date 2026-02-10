"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class JobCreate(BaseModel):
    """Request schema for creating a transcription job."""
    filename: str
    model: str = "base"
    language: Optional[str] = None


class SegmentSchema(BaseModel):
    """Schema for a transcription segment."""
    start_time: float
    end_time: float
    text: str
    speaker: str
    confidence: float


class JobResult(BaseModel):
    """Response schema for completed transcription job."""
    job_id: str
    status: str
    filename: str
    text: str
    segments: List[SegmentSchema]
    speakers: int
    duration: float


class JobStatus(BaseModel):
    """Response schema for job status check."""
    job_id: str
    status: str  # queued, processing, completed, failed
    result: Optional[JobResult] = None


class TranscriptionHistoryItem(BaseModel):
    """Schema for history list item."""
    job_id: str
    filename: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    speakers_detected: int
    duration: Optional[float]


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    error: str
    message: str