"""Tests for database models."""
import pytest
from datetime import datetime

from app.models import Base, TranscriptionJob, Segment


class TestTranscriptionJob:
    """Tests for TranscriptionJob model."""

    def test_create_transcription_job(self):
        """Should create a transcription job with all fields."""
        job = TranscriptionJob(
            id="test-job-123",
            filename="test_audio.mp3",
            original_path="/tmp/test_audio.mp3",
            status="queued",
            model="base",
            language="en"
        )

        assert job.id == "test-job-123"
        assert job.filename == "test_audio.mp3"
        assert job.original_path == "/tmp/test_audio.mp3"
        assert job.status == "queued"
        assert job.model == "base"
        assert job.language == "en"
        assert job.speakers_detected == 0  # Default value
        assert job.duration is None  # Default value
        assert job.created_at is not None

    def test_transcription_job_defaults(self):
        """Should have correct default values."""
        job = TranscriptionJob(id="test-job")
        assert job.status == "queued"  # Default status
        assert job.speakers_detected == 0  # Default speakers
        assert job.duration is None  # Default duration
        assert job.language is None  # Default language
        assert job.created_at is not None

    def test_transcription_job_relationship(self):
        """Should have segments relationship."""
        job = TranscriptionJob(id="test-job")
        assert hasattr(job, 'segments')
        assert job.segments == []  # Should be empty list


class TestSegment:
    """Tests for Segment model."""

    def test_create_segment(self):
        """Should create a segment with all fields."""
        segment = Segment(
            id=1,
            job_id="test-job-123",
            start_time=0.0,
            end_time=5.5,
            text="Hello world",
            speaker="SPEAKER_00",
            confidence=0.95
        )

        assert segment.id == 1
        assert segment.job_id == "test-job-123"
        assert segment.start_time == 0.0
        assert segment.end_time == 5.5
        assert segment.text == "Hello world"
        assert segment.speaker == "SPEAKER_00"
        assert segment.confidence == 0.95

    def test_segment_relationship(self):
        """Should have job relationship."""
        segment = Segment(
            id=1,
            job_id="test-job-123",
            start_time=0.0,
            end_time=5.5,
            text="Hello",
            speaker="SPEAKER_00",
            confidence=0.95
        )

        assert hasattr(segment, 'job')


class TestDatabaseBase:
    """Tests for database base configuration."""

    def test_base_has_tables_attribute(self):
        """Base should have tables attribute for model metadata."""
        assert hasattr(Base, '__tablename__') is False  # Base itself has no table name
        assert hasattr(Base, 'metadata')

    def test_models_have_tablename(self):
        """Models should have __tablename__ defined."""
        assert TranscriptionJob.__tablename__ == "transcriptionjob"
        assert Segment.__tablename__ == "segment"

    def test_models_have_primary_key(self):
        """Models should have primary keys defined."""
        assert hasattr(TranscriptionJob, 'id')
        assert hasattr(Segment, 'id')

    def test_models_have_relationships(self):
        """Models should have relationships defined."""
        assert hasattr(TranscriptionJob, 'segments')
        assert hasattr(Segment, 'job')