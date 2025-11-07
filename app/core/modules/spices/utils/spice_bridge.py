
"""
app/core/modules/spices/utils/spice_bridge.py

Smart bridge between the main recipes DB and the spices DB.
It automatically detects whether the environment is running in testing
or production mode and adjusts connections accordingly.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.db_manager import Recipe, engine as main_engine
from app.core.modules.spices.db.spices_models import (
    SessionLocal as SpiceSessionLocal,
    engine as spice_engine,
    Base as SpiceBase,
)
from app.core import db_manager

# ------------------------------------------------------
# 🧠 Dynamic environment-aware DB routing
# ------------------------------------------------------

def get_main_session():
    """
    Return a Session for the main DB.
    Automatically uses in-memory SQLite when running under pytest.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        
        SessionLocal = sessionmaker(bind=main_engine)
        return SessionLocal()
    else:
        return db_manager.SessionLocal()


def get_spice_session():
    """
    Return a Session for the spices DB.

    During pytest, this reuses the patched SessionLocal 
    defined in app.core.modules.spices.db.spices_models, 
    which conftest.py overrides to use a shared in-memory engine.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:

        return SpiceSessionLocal()

    SessionLocal = sessionmaker(bind=spice_engine)
    return SessionLocal()

# ------------------------------------------------------
# 🔗 Bridge Logic
# ------------------------------------------------------

def get_recipe_from_main(recipe_name: str):
    """Fetch a recipe by name from the main (recipes) DB using the ORM model."""
    session = get_main_session()
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()
    session.close()
    return recipe


def link_spice_to_recipe(spice_name: str, recipe_name: str):
    """Validate both spice and recipe exist across their DBs."""
    recipe = get_recipe_from_main(recipe_name)
    spice_session = get_spice_session()
    spice = spice_session.query(Spice).filter_by(name=spice_name).first()
    spice_session.close()

    if not recipe:
        return {"status": "error", "message": f"Recipe '{recipe_name}' not found."}
    if not spice:
        return {"status": "error", "message": f"Spice '{spice_name}' not found."}

    return {
        "status": "success",
        "message": f"Linked spice '{spice_name}' → recipe '{recipe_name}'."
    }


def suggest_spices_for_recipe(recipe_name: str):
    """Suggest spices that pair well with a given recipe."""
    recipe = get_recipe_from_main(recipe_name)
    if not recipe:
        return {"status": "error", "message": f"Recipe '{recipe_name}' not found."}

    spice_session = get_spice_session()
    spices = spice_session.query(Spice).all()
    spice_session.close()

    matching = [
        s.name for s in spices
        if recipe.name in (s.pairs_with_recipes or []) or
           any(ing.name in (s.pairs_with_ingredients or []) for ing in getattr(recipe, "ingredients", []))
    ]

    return {"status": "success", "data": matching}
