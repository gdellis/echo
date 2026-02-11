"""Pytest configuration and fixtures for backend tests."""
import os
import pytest
import tempfile

_original_get_session = None


@pytest.fixture(scope="session", autouse=True)
def setup_test_settings():
    """Set up test settings for all tests - runs before any test."""
    import app.config
    from app.utils.file_ops import get_database_engine
    import app.models
    from app.models import Base
    
    # Store original values
    original_url = app.config.settings.DATABASE_URL
    
    # Create a temporary database file for all tests
    temp_db = os.path.join(tempfile.gettempdir(), "transcriber_test.db")
    
    # Patch settings with test values - direct attribute assignment
    app.config.settings.DATABASE_URL = f"sqlite:///{temp_db}"
    app.config.settings.UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "transcriber_test_uploads")
    
    # Create test database engine
    engine = get_database_engine()
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Drop all tables after all tests
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    
    # Remove temp files
    try:
        if os.path.exists(temp_db):
            os.remove(temp_db)
    except:
        pass
    
    # Restore original settings
    app.config.settings.DATABASE_URL = original_url


@pytest.fixture(scope="function")
def test_client():
    """Create test client with patched database session."""
    import app.config
    import app.utils.file_ops as file_ops_module
    from fastapi.testclient import TestClient
    
    # Create a test session factory
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(
        app.config.settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def patched_get_session():
        """Get test database session."""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Store the original function reference before patching
    global _original_get_session
    _original_get_session = file_ops_module.get_session
    
    # Patch get_session with a wrapper that creates a new session each time
    def get_session_wrapper():
        return next(patched_get_session())
    
    file_ops_module.get_session = get_session_wrapper
    
    # Import the app (after patching)
    from app.main import app
    
    # Use the TestClient with app as positional argument
    client = TestClient(app)
    yield client
    
    # Restore original get_session
    file_ops_module.get_session = _original_get_session


@pytest.fixture(scope="function")
def db_session():
    """Create a database session for a test."""
    import app.config
    
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(
        app.config.settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()