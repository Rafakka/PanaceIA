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
from app.core.modules.spices.db import spices_models
from app.core.db_manager import Base
from app.core.db_manager import engine as main_engine
from sqlalchemy.orm import close_all_sessions

# ---------------------------------------------------------------------------
# 1. DATABASE FIXTURE — shared in-memory SQLite engine for tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function", autouse=True)
def setup_test_dbs(monkeypatch):
    """
    Recreates clean recipe + spice databases before each test.
    Ensures both engines share the same lifecycle so data doesn’t persist between tests.
    """
    main_engine = db_manager.engine
    MainSessionLocal = sessionmaker(bind=main_engine)

    db_manager.Base.metadata.drop_all(bind=main_engine)
    db_manager.Base.metadata.create_all(bind=main_engine)

    def override_main_session():
        return MainSessionLocal()

    monkeypatch.setattr("app.core.db_manager.SessionLocal", override_main_session)

    spice_engine = spices_models.engine
    SpiceSessionLocal = sessionmaker(bind=spice_engine)

    spices_models.Base.metadata.drop_all(bind=spice_engine)
    spices_models.Base.metadata.create_all(bind=spice_engine)

    def override_spice_session():
        return SpiceSessionLocal()

    monkeypatch.setattr(
        "app.core.modules.spices.db.spices_models.SessionLocal",
        override_spice_session,
    )

    try:
        yield
    finally:
        close_all_sessions()
        main_engine.dispose()
        spice_engine.dispose()

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
        
@pytest.fixture(scope="session", autouse=False)
def legacy_db_setup():
    from app.core.db_manager import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)