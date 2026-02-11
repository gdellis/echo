"""
API routes for the Transcriber backend (v1).
"""
import os
import uuid
import shutil
from typing import Optional

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.models import TranscriptionJob, Segment
from app.utils.file_ops import (
    generate_job_id, 
    is_valid_audio_format, 
    get_file_size,
    cleanup_temp_files,
    get_database_engine,
    get_session
)

router = APIRouter(prefix="/api/v1", tags=["transcription"])


# Database dependency that can be overridden in tests
def get_db():
    """Get database session dependency."""
    db = get_session()
    try:
        yield db
    finally:
        db.close()

# Lazy imports for Celery tasks (to avoid importing torch on module load)
_process_transcription = None
_delete_job = None

def _get_process_transcription():
    """Lazy load process_transcription task."""
    global _process_transcription
    if _process_transcription is None:
        from app.tasks.tasks import process_transcription
        _process_transcription = process_transcription
    return _process_transcription

def _get_delete_job():
    """Lazy load delete_job task."""
    global _delete_job
    if _delete_job is None:
        from app.tasks.tasks import delete_job
        _delete_job = delete_job
    return _delete_job


@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    model: Optional[str] = "base",
    language: Optional[str] = None
):
    """
    Upload and transcribe an audio file.
    
    Args:
        file: Audio file to transcribe
        model: Whisper model to use (base, small, medium, large)
        language: Language code (optional)
    
    Returns:
        Job ID for tracking progress
    """
    # Check file extension
    if not is_valid_audio_format(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported formats: mp3, wav, mp4, mov, m4a, flac"
        )
    
    # Check file size
    file_size = len(await file.read())
    await file.seek(0)  # Reset file pointer
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE / (1024 * 1024)}MB"
        )
    
    # Generate job ID
    job_id = generate_job_id()
    
    # Save uploaded file temporarily
    temp_dir = "/tmp/transcriber"
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_path = os.path.join(temp_dir, f"{job_id}_{file.filename}")
    
    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Create job record in database
        from sqlalchemy.orm import Session
        from app.utils.file_ops import get_session
        
        db = get_session()
        try:
            job = TranscriptionJob(
                id=job_id,
                filename=file.filename,
                original_path=temp_path,
                status="queued",
                model=model,
                language=language
            )
            db.add(job)
            db.commit()
        finally:
            db.close()
        
        # Queue the transcription task
        _get_process_transcription().delay(job_id, temp_path, file.filename, model, language)
        
        return {
            "job_id": job_id,
            "status": "queued",
            "message": "File uploaded, processing started"
        }
        
    except Exception as e:
        cleanup_temp_files(temp_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    """
    Check job status and get results.
    
    Args:
        job_id: The ID of the transcription job
    
    Returns:
        Job status and results if completed
    """
    from app.utils.file_ops import get_session
    
    db = get_session()
    try:
        job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        result = {
            "job_id": job.id,
            "status": job.status,
            "filename": job.filename,
            "created_at": job.created_at
        }
        
        if job.status == "completed":
            segments = db.query(Segment).filter(Segment.job_id == job_id).all()
            
            # Build full text
            text = " ".join(seg.text for seg in segments)
            
            # Build segments list
            segments_list = [
                {
                    "start": seg.start_time,
                    "end": seg.end_time,
                    "text": seg.text,
                    "speaker": seg.speaker,
                    "confidence": seg.confidence
                }
                for seg in segments
            ]
            
            result["result"] = {
                "text": text,
                "segments": segments_list,
                "speakers": job.speakers_detected,
                "duration": job.duration
            }
        
        elif job.status == "failed":
            result["error"] = "Transcription failed"
        
        return result
        
    finally:
        db.close()


@router.get("/history")
def get_history(
    limit: int = 10,
    offset: int = 0
):
    """
    List all transcriptions with metadata.
    
    Args:
        limit: Maximum number of results
        offset: Number of results to skip
    
    Returns:
        List of transcription jobs
    """
    from app.utils.file_ops import get_session
    
    db = get_session()
    try:
        jobs = db.query(TranscriptionJob).order_by(
            TranscriptionJob.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return {
            "jobs": [
                {
                    "job_id": job.id,
                    "filename": job.filename,
                    "status": job.status,
                    "created_at": job.created_at,
                    "completed_at": job.completed_at,
                    "speakers_detected": job.speakers_detected,
                    "duration": job.duration
                }
                for job in jobs
            ]
        }
        
    finally:
        db.close()


@router.delete("/jobs/{job_id}")
def delete_transcription(job_id: str):
    """
    Delete a transcription job and associated files.
    
    Args:
        job_id: The ID of the transcription job to delete
    
    Returns:
        Deletion confirmation
    """
    from app.utils.file_ops import get_session
    
    db = get_session()
    try:
        job = db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Queue deletion task
        _get_delete_job().delay(job_id)
        
        return {
            "message": "Deletion requested",
            "job_id": job_id
        }
        
    finally:
        db.close()