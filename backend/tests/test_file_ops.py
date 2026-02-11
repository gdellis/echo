"""Tests for file operations utilities."""
import os
import tempfile
import shutil
import pytest

from app.utils.file_ops import (
    generate_job_id,
    is_valid_audio_format,
    get_file_extension,
    get_file_size,
    format_duration,
    cleanup_temp_files,
)


class TestGenerateJobId:
    """Tests for generate_job_id function."""

    def test_generate_job_id_returns_unique_ids(self):
        """Each call should return a unique UUID."""
        id1 = generate_job_id()
        id2 = generate_job_id()
        assert id1 != id2

    def test_generate_job_id_is_string(self):
        """Generated ID should be a string."""
        job_id = generate_job_id()
        assert isinstance(job_id, str)

    def test_generate_job_id_format(self):
        """Generated ID should follow UUID format."""
        job_id = generate_job_id()
        # Should contain hyphens in UUID format
        assert "-" in job_id


class TestIsValidAudioFormat:
    """Tests for is_valid_audio_format function."""

    @pytest.mark.parametrize("filename", [
        "audio.mp3",
        "video.WAV",
        "file.Mp4",
        "clip.MOV",
        "audio.m4a",
        "sound.FLAC",
    ])
    def test_valid_formats(self, filename):
        """Should return True for valid audio formats."""
        assert is_valid_audio_format(filename) is True

    @pytest.mark.parametrize("filename", [
        "document.pdf",
        "image.jpg",
        "text.txt",
        "video.avi",  # Not in supported list
        "archive.zip",
    ])
    def test_invalid_formats(self, filename):
        """Should return False for non-audio formats."""
        assert is_valid_audio_format(filename) is False

    def test_empty_filename(self):
        """Should return False for empty filename."""
        assert is_valid_audio_format("") is False

    def test_filename_without_extension(self):
        """Should return False for filename without extension."""
        assert is_valid_audio_format("noextension") is False


class TestGetFileExtension:
    """Tests for get_file_extension function."""

    def test_returns_lowercase_extension(self):
        """Extension should be returned in lowercase without dot."""
        assert get_file_extension("audio.MP3") == "mp3"
        assert get_file_extension("video.WAV") == "wav"

    def test_returns_extension_with_dot_stripped(self):
        """Dot should be stripped from extension."""
        assert get_file_extension("file.mp3") == "mp3"

    def test_returns_empty_for_no_extension(self):
        """Should return empty string for no extension."""
        assert get_file_extension("noextension") == ""

    def test_handles_multiple_dots(self):
        """Should handle filenames with multiple dots."""
        assert get_file_extension("file.name.tar.gz") == "gz"


class TestGetFileSize:
    """Tests for get_file_size function."""

    def test_returns_size_in_bytes(self):
        """Should return file size in bytes."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"Hello, World!")
            temp_path = f.name

        try:
            size = get_file_size(temp_path)
            assert size == 13  # "Hello, World!" is 13 bytes
        finally:
            os.unlink(temp_path)

    def test_returns_zero_for_empty_file(self):
        """Should return 0 for empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            size = get_file_size(temp_path)
            assert size == 0
        finally:
            os.unlink(temp_path)


class TestFormatDuration:
    """Tests for format_duration function."""

    def test_formats_seconds(self):
        """Should format seconds correctly."""
        assert format_duration(5) == "00:00:05"

    def test_formats_minutes_and_seconds(self):
        """Should format minutes and seconds correctly."""
        assert format_duration(65) == "00:01:05"  # 1 min 5 sec

    def test_formats_hours_minutes_seconds(self):
        """Should format hours, minutes, and seconds correctly."""
        assert format_duration(3665) == "01:01:05"  # 1 hour 1 min 5 sec

    def test_formats_zero(self):
        """Should format zero correctly."""
        assert format_duration(0) == "00:00:00"

    def test_large_duration(self):
        """Should handle large durations."""
        assert format_duration(86400) == "24:00:00"  # 24 hours


class TestCleanupTempFiles:
    """Tests for cleanup_temp_files function."""

    def test_removes_existing_file(self):
        """Should remove existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        assert os.path.exists(temp_path)
        cleanup_temp_files(temp_path)
        assert not os.path.exists(temp_path)

    def test_handles_nonexistent_file(self):
        """Should handle nonexistent file without error."""
        nonexistent_path = "/tmp/nonexistent_file_12345.txt"
        assert not os.path.exists(nonexistent_path)
        # Should not raise an exception
        cleanup_temp_files(nonexistent_path)

    def test_handles_directory(self):
        """Should clean up directory contents."""
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "test_file.txt")
        with open(temp_file, "w") as f:
            f.write("test")

        assert os.path.exists(temp_file)
        cleanup_temp_files(temp_file)
        assert not os.path.exists(temp_file)
        # Clean up directory
        shutil.rmtree(temp_dir)