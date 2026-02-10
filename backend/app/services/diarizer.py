"""
Speaker diarization service using pyannote.audio.
"""
import os
import logging
from typing import List, Dict, Optional

import torch

logger = logging.getLogger(__name__)


class Diarizer:
    """Service for speaker diarization using pyannote.audio."""
    
    def __init__(self, model: str = "pyannote/speaker-diarization"):
        """
        Initialize the diarizer.
        
        Args:
            model: pyannote.audio model to use
        """
        self.model_name = model
        self.pipeline = None
        logger.info(f"Initializing pyannote.audio model: {model}")
    
    def _load_pipeline(self):
        """Load the pyannote.audio pipeline (lazy loading)."""
        if self.pipeline is None:
            from pyannote.audio import Pipeline
            self.pipeline = Pipeline.from_pretrained(
                self.model_name,
                use_auth_token=os.getenv("HF_AUTH_TOKEN")
            )
        return self.pipeline
    
    def diarize(self, audio_path: str) -> dict:
        """
        Perform speaker diarization on an audio file.
        
        Args:
            audio_path: Path to the audio file
        
        Returns:
            dict: Diarization result with speaker segments
        """
        pipeline = self._load_pipeline()
        
        logger.info(f"Running speaker diarization on: {audio_path}")
        
        # Run diarization
        diarization = pipeline(audio_path)
        
        # Convert to standard format
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })
        
        return {
            "segments": segments,
            "num_speakers": len(set(seg["speaker"] for seg in segments))
        }
    
    def align_segments(self, 
                       transcription_segments: List[Dict], 
                       diarization_segments: List[Dict]) -> List[Dict]:
        """
        Align transcription segments with speaker labels from diarization.
        
        Args:
            transcription_segments: List of transcription segments with text
            diarization_segments: List of diarization segments with speakers
        
        Returns:
            List[Dict]: Aligned segments with text and speaker labels
        """
        aligned = []
        
        for t_seg in transcription_segments:
            t_start = t_seg["start"]
            t_end = t_seg["end"]
            t_text = t_seg["text"]
            
            # Find the speaker who spoke during this segment
            speaker = self._find_speaker_for_segment(t_start, t_end, diarization_segments)
            
            aligned.append({
                "start": t_start,
                "end": t_end,
                "text": t_text,
                "speaker": speaker,
                "confidence": t_seg.get("confidence", 0.95)
            })
        
        return aligned
    
    def _find_speaker_for_segment(self, 
                                   start: float, 
                                   end: float, 
                                   diarization_segments: List[Dict]) -> str:
        """
        Find the dominant speaker for a given time segment.
        
        Args:
            start: Segment start time
            end: Segment end time
            diarization_segments: List of diarization segments
        
        Returns:
            str: Speaker label
        """
        # Calculate intersection with each diarization segment
        overlaps = []
        for d_seg in diarization_segments:
            d_start = d_seg["start"]
            d_end = d_seg["end"]
            
            # Calculate overlap
            overlap_start = max(start, d_start)
            overlap_end = min(end, d_end)
            
            if overlap_start < overlap_end:
                overlap = overlap_end - overlap_start
                overlaps.append({
                    "speaker": d_seg["speaker"],
                    "overlap": overlap
                })
        
        if not overlaps:
            return "SPEAKER_00"
        
        # Return the speaker with the most overlap
        speaker = max(overlaps, key=lambda x: x["overlap"])["speaker"]
        return speaker