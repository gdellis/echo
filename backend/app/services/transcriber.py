"""
Transcription service using OpenAI Whisper.
"""
import os
import logging
from typing import Optional

import whisper

logger = logging.getLogger(__name__)


class Transcriber:
    """Service for transcribing audio using Whisper."""
    
    def __init__(self, model: str = "base"):
        """
        Initialize the transcriber.
        
        Args:
            model: Whisper model to use (base, small, medium, large)
        """
        self.model_name = model
        self.model = None
        logger.info(f"Initializing Whisper model: {model}")
    
    def _load_model(self):
        """Load the Whisper model (lazy loading)."""
        if self.model is None:
            self.model = whisper.load_model(self.model_name)
        return self.model
    
    def transcribe(self, audio_path: str, language: Optional[str] = None) -> dict:
        """
        Transcribe an audio file.
        
        Args:
            audio_path: Path to the audio file
            language: Language code (optional, auto-detected if None)
        
        Returns:
            dict: Transcription result with text and segments
        """
        model = self._load_model()
        
        logger.info(f"Transcribing audio file: {audio_path}")
        
        # Transcribe the audio
        result = model.transcribe(
            audio_path,
            language=language,
            word_timestamps=True
        )
        
        # Convert to standard format
        segments = []
        for seg in result["segments"]:
            segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
                "confidence": 0.95  # Whisper doesn't provide confidence scores
            })
        
        return {
            "text": result["text"],
            "segments": segments,
            "duration": result.get("duration", 0),
            "language": result.get("language", "unknown")
        }