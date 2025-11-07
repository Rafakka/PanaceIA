# app/core/modules/spices/utils/spice_bridge.py
"""
Bridge utility between the main (recipes) DB and the spices DB.
Used for logical linking in both runtime and tests.
"""

from app.core.db_manager import SessionLocal as MainSession
from app.core.db_manager import Recipe
from app.core.modules.spices.db.spices_models import SessionLocal as SpiceSession, Spice


def link_spice_to_recipe(spice_name: str, recipe_name: str):
    """
    Logically links a spice from the spices DB to a recipe from the main DB.

    This does not physically join the two databases — instead, it simulates a
    bridge that validates the existence of both entities.

    Returns:
        dict: status and message about the linking process.
    """
    main_session = MainSession()
    spice_session = SpiceSession()

    recipe = main_session.query(Recipe).filter_by(name=recipe_name).first()
    spice = spice_session.query(Spice).filter_by(name=spice_name).first()

    if not recipe:
        return {"status": "error", "message": f"Recipe '{recipe_name}' not found."}
    if not spice:
        return {"status": "error", "message": f"Spice '{spice_name}' not found."}

    return {"status": "success", "message": f"Linked spice '{spice_name}' → recipe '{recipe_name}'."}
