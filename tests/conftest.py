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
import importlib
import app.core.modules.spices.utils.spice_bridge as spice_bridge
importlib.reload(spice_bridge)

import pytest
from sqlalchemy.orm import sessionmaker, Session, close_all_sessions
from fastapi.testclient import TestClient
from app.main import app
from app.core import db_manager
from app.core.db_manager import Base, engine as main_engine
from app.core.modules.spices.db import spices_models


@pytest.fixture(scope="function", autouse=True)
def setup_test_dbs(monkeypatch):
    """
    Creates isolated in-memory versions of both the main (recipes) and spices databases.
    Ensures bridge utilities and endpoints share the same database context.
    """

    # 1️⃣ Create session factory for main DB
    MainSessionLocal = sessionmaker(bind=main_engine)

    def override_main_session():
        return MainSessionLocal()

    # Patch SessionLocal so app and tests use this factory
    monkeypatch.setattr("app.core.db_manager.SessionLocal", override_main_session)

    # 2️⃣ Reset main DB schema
    Base.metadata.drop_all(bind=main_engine)
    Base.metadata.create_all(bind=main_engine)

    # 3️⃣ Reset spices DB schema
    spice_engine = spices_models.engine
    SpiceSessionLocal = sessionmaker(bind=spice_engine)
    spices_models.Base.metadata.drop_all(bind=spice_engine)
    spices_models.Base.metadata.create_all(bind=spice_engine)

    def override_spice_session():
        return SpiceSessionLocal()

    monkeypatch.setattr(
        "app.core.modules.spices.db.spices_models.SessionLocal",
        override_spice_session
    )

    try:
        yield
    finally:
        close_all_sessions()


# ---------------------------------------------------------------------------
# 2️⃣ FASTAPI TEST CLIENT
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as client:
        yield client


# ---------------------------------------------------------------------------
# 3️⃣ LEGACY (OPTIONAL)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=False)
def legacy_db_setup():
    from app.core.db_manager import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
