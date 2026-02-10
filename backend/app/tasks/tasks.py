"""
Celery tasks for transcription and speaker diarization.
"""
import os
import uuid
import tempfile
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from celery import current_task
import torch

from app.config import settings
from app.models import TranscriptionJob, Segment, Base
from app.services.transcriber import Transcriber
from app.services.diarizer import Diarizer
from app.utils.file_ops import get_database_engine
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


def get_session():
    """Get database session."""
    engine = get_database_engine()
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def init_db():
    """Initialize database tables."""
    engine = get_database_engine()
    Base.metadata.create_all(bind=engine)


@current_task.task_prerun.connect
def on_task_prerun(sender=None, task_id=None, task=None, **kwargs):
    """Initialize db connection before task runs."""
    init_db()


@current_task.task_postrun.connect
def on_task_postrun(sender=None, task_id=None, task=None, retval=None, **kwargs):
    """Close db connection after task runs."""
    pass


@celery_app.task(bind=True)
def process_transcription(self, job_id: str, file_path: str, filename: str, 
                          model: str = "base", language: Optional[str] = None):
    """
    Celery task to process audio transcription with speaker diarization.
    
    Args:
        job_id: The ID of the transcription job
        file_path: Path to the audio file
        filename: Original filename
        model: Whisper model to use (base, small, medium, large)
        language: Language code (optional)
    
    Returns:
        dict: Processing results
    """
    logger.info(f"Starting transcription job: {job_id}")
    
    session = get_session()
    
    try:
        # Update job status
        job = session.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
        if job:
            job.status = "processing"
            session.commit()
        
        # Initialize services
        transcriber = Transcriber(model=model)
        diarizer = Diarizer()
        
        # Step 1: Transcribe with Whisper
        logger.info(f"Transcribing with Whisper model: {model}")
        transcript_result = transcriber.transcribe(file_path, language)
        
        # Step 2: Run speaker diarization
        logger.info("Running speaker diarization")
        diarization_result = diarizer.diarize(file_path)
        
        # Step 3: Align diarization with transcription
        logger.info("Aligning transcription with speaker labels")
        aligned_segments = diarizer.align_segments(
            transcript_result["segments"],
            diarization_result
        )
        
        # Calculate duration
        duration = transcript_result.get("duration", 0)
        
        # Count speakers
        speakers = len(set(seg["speaker"] for seg in aligned_segments))
        
        # Store results in database
        job.completed_at = datetime.utcnow()
        job.status = "completed"
        job.duration = duration
        job.speakers_detected = speakers
        session.commit()
        
        # Store segments
        for seg in aligned_segments:
            segment = Segment(
                job_id=job_id,
                start_time=seg["start"],
                end_time=seg["end"],
                text=seg["text"],
                speaker=seg["speaker"],
                confidence=seg["confidence"]
            )
            session.add(segment)
        
        session.commit()
        
        logger.info(f"Transcription job completed: {job_id}")
        
        return {
            "job_id": job_id,
            "status": "completed",
            "filename": filename,
            "text": transcript_result["text"],
            "segments": aligned_segments,
            "speakers": speakers,
            "duration": duration
        }
        
    except Exception as e:
        logger.error(f"Error processing transcription {job_id}: {str(e)}")
        
        # Update job status to failed
        if job:
            job.status = "failed"
            session.commit()
        
        raise
    
    finally:
        session.close()


@celery_app.task
def delete_job(job_id: str):
    """
    Celery task to delete a transcription job and its associated files.
    
    Args:
        job_id: The ID of the transcription job to delete
    """
    session = get_session()
    
    try:
        job = session.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
        if job:
            # Delete associated segments
            session.query(Segment).filter(Segment.job_id == job_id).delete()
            
            # Delete the job
            session.delete(job)
            session.commit()
            
            # Delete the file
            if os.path.exists(job.original_path):
                os.remove(job.original_path)
                
        return {"status": "deleted", "job_id": job_id}
        
    except Exception as e:
        logger.error(f"Error deleting job {job_id}: {str(e)}")
        session.rollback()
        raise
    finally:
        session.close()