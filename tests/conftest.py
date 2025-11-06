"""
PanaceIA Test Configuration
===========================

This file defines the pytest fixtures that power the automated test suite.
It ensures every test runs in isolation with a clean, shared in-memory SQLite
database and a fresh FastAPI TestClient instance.

Key Fixtures
-------------
- setup_test_db: Automatically sets up and tears down the test database before
  and after each test. Patches SessionLocal so all managers use the same engine.
- test_client: Provides a FastAPI TestClient connected to the in-memory database.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core import db_manager
from app.core.modules.spices.db.spices_models import Spice
from app.core.db_manager import Base, engine

# ---------------------------------------------------------------------------
# 1. DATABASE FIXTURE — shared in-memory SQLite engine for tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function", autouse=True)
def setup_test_db(monkeypatch):
    """
    Creates a shared in-memory SQLite database and patches SessionLocal
    so every test runs with a clean schema and isolated transaction.

    This fixture runs automatically for every test function.
    """

    # Create a shared in-memory database accessible across threads
    test_engine = create_engine(
        "sqlite:///file::memory:?cache=shared",
        echo=False,
        connect_args={"check_same_thread": False},  # allow FastAPI thread access
    )

    # Create a session factory bound to this engine
    TestingSessionLocal = sessionmaker(bind=test_engine)

    # Create all tables for the tests
    db_manager.Base.metadata.create_all(test_engine)

    # Patch the SessionLocal in db_manager to point to our test session
    def override_session():
        return TestingSessionLocal()

    monkeypatch.setattr("app.core.db_manager.SessionLocal", override_session)

    yield  # ---- Run the test ----

    # Drop all tables after each test to ensure a clean state
    db_manager.Base.metadata.drop_all(test_engine)


# ---------------------------------------------------------------------------
# 2. FASTAPI TEST CLIENT FIXTURE
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def test_client():
    """
    Provides a FastAPI TestClient that interacts with the test database.
    Each test gets a new, isolated client context.

    Usage:
        def test_example(test_client):
            res = test_client.get("/ingredients/")
            assert res.status_code == 200
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Ensure all tables (including spices) exist for tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)