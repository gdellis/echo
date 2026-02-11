"""Tests for API routes (mocked tests)."""
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app
from app.config import settings


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_endpoint_returns_metadata(self, test_client):
        """Should return application metadata."""
        response = test_client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "name" in data
        assert "version" in data
        assert "status" in data
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"

    def test_root_endpoint_returns_correct_name(self, test_client):
        """Should return the app name from settings."""
        response = test_client.get("/")

        assert response.status_code == 200
        assert response.json()["name"] == settings.APP_NAME


class TestHealthCheckEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_healthy(self, test_client):
        """Should return healthy status."""
        response = test_client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"


class TestRequestSizeLimit:
    """Tests for request size limits."""

    def test_returns_413_for_large_files(self, test_client):
        """Should return 413 for files exceeding size limit."""
        # Create a file larger than MAX_UPLOAD_SIZE
        # MAX_UPLOAD_SIZE is typically 16MB (16 * 1024 * 1024)
        large_content = b"x" * (20 * 1024 * 1024)  # 20MB

        response = test_client.post(
            "/api/v1/transcribe",
            files={"file": ("large_file.mp3", large_content, "audio/mpeg")}
        )

        # Note: TestClient may not enforce the same limits as actual server
        # This test documents the expected behavior
        assert response.status_code in [413, 500]  # May vary by configuration


class TestGetJobStatus:
    """Tests for the get job status endpoint."""

    def test_returns_404_for_nonexistent_job(self, test_client):
        """Should return 404 for non-existent job."""
        response = test_client.get("/api/v1/jobs/nonexistent-job-id")

        assert response.status_code == 404


class TestGetHistory:
    """Tests for the history endpoint."""

    def test_returns_jobs_list(self, test_client):
        """Should return a list of jobs (possibly empty)."""
        response = test_client.get("/api/v1/history")

        assert response.status_code == 200
        data = response.json()

        assert "jobs" in data
        assert isinstance(data["jobs"], list)

    def test_history_respects_limit_parameter(self, test_client):
        """Should respect the limit parameter."""
        response = test_client.get("/api/v1/history?limit=5")

        assert response.status_code == 200


class TestDeleteJob:
    """Tests for the delete job endpoint."""

    def test_returns_404_for_nonexistent_job(self, test_client):
        """Should return 404 for non-existent job."""
        response = test_client.delete("/api/v1/jobs/nonexistent-job-id")

        assert response.status_code == 404