"""
app/core/modules/spices/utils/spice_bridge.py

Bridge between the main recipes DB and the spices DB.
Ensures both databases communicate correctly in tests and production.
"""

from app.core import db_manager
from app.core.modules.spices.db.spices_models import (
    Spice,
    SessionLocal as SpiceSessionLocal,
)
from sqlalchemy import func

# ------------------------------------------------------
# 🧠 Sessions for both DBs
# ------------------------------------------------------

def get_main_session():
    """Return a session for the main recipes database."""
    return db_manager.SessionLocal()


def get_spice_session():
    """Return a session for the spices database."""
    return SpiceSessionLocal()


# ------------------------------------------------------
# 🔗 Bridge Logic
# ------------------------------------------------------

def get_recipe_from_main(recipe_name: str):
    """Fetch a recipe from the main database by name."""
    from app.core.db_manager import Recipe
    session = get_main_session()
    try:
        recipe = session.query(Recipe).filter_by(name=recipe_name).first()
        if not recipe:
            print(f"❌ Recipe '{recipe_name}' not found in main DB.")
            return None
        print(f"✅ Found recipe '{recipe_name}' in main DB.")
        return recipe
    except Exception as e:
        print(f"⚠️ Error fetching recipe '{recipe_name}': {e}")
        return None
    finally:
        session.close()

def link_spice_to_recipe(spice_name: str, recipe_name: str):
    """Validate both spice and recipe exist across their DBs."""
    print(f"🔗 Linking spice '{spice_name}' → recipe '{recipe_name}'")

    recipe = get_recipe_from_main(recipe_name)
    if not recipe:
        print(f"❌ Recipe '{recipe_name}' not found in main DB.")
        return {"status": "error", "message": f"Recipe '{recipe_name}' not found."}

    spice_session = get_spice_session()
    spices = spice_session.query(Spice).all()

    print("\n🧂 [DEBUG] SPICES SNAPSHOT:")
    for s in spices:
        print(f"   -> id={s.id}, name={s.name!r}, type={type(s.name)}, flavor_profile={s.flavor_profile!r}")

    spice = next((s for s in spices if s.name.strip().lower() == spice_name.strip().lower()), None)

    if not spice:
        print(f"❌ Spice '{spice_name}' not found in spice DB.")
        spice_session.close()
        return {"status": "error", "message": f"Spice '{spice_name}' not found."}

    spice_session.close()
    print(f"✅ Linked spice '{spice.name}' → recipe '{recipe.name}' successfully.")
    return {
        "status": "success",
        "message": f"Linked spice '{spice.name}' → recipe '{recipe.name}'."
    }

def unlink_spice_from_recipe(spice_name: str, recipe_name: str):
    """Simulate unlinking a spice from a recipe."""
    print(f"🔗 Unlinking spice '{spice_name}' ← recipe '{recipe_name}'")

    recipe = get_recipe_from_main(recipe_name)
    if not recipe:
        print(f"❌ Recipe '{recipe_name}' not found in main DB.")
        return {"status": "error", "message": f"Recipe '{recipe_name}' not found."}

    spice_session = get_spice_session()
    spices = spice_session.query(Spice).all()

    spice = next((s for s in spices if s.name.strip().lower() == spice_name.strip().lower()), None)
    if not spice:
        print(f"❌ Spice '{spice_name}' not found in spice DB.")
        spice_session.close()
        return {"status": "error", "message": f"Spice '{spice_name}' not found."}

    print(f"✅ Unlinked spice '{spice.name}' ← recipe '{recipe.name}' successfully.")
    spice_session.close()
    return {
        "status": "success",
        "message": f"Unlinked spice '{spice.name}' ← recipe '{recipe.name}' successfully."
    }


def suggest_spices_for_recipe(recipe_name: str):
    """Suggest spices that pair well with a given recipe."""
    print(f"🧠 Suggesting spices for recipe '{recipe_name}'")

    recipe = get_recipe_from_main(recipe_name)
    if not recipe:
        print(f"❌ Recipe '{recipe_name}' not found in main DB.")
        return []

    spice_session = get_spice_session()
    spices = spice_session.query(Spice).all()

    print("🧂 [DEBUG] Checking spices for matching pairs...")
    suggestions = []

    for s in spices:
        
        pairs_with_recipes = []
        pairs_with_ingredients = []

        if isinstance(s.pairs_with_recipes, str):
            pairs_with_recipes = [r.strip().lower() for r in s.pairs_with_recipes.split(",") if r.strip()]
        elif isinstance(s.pairs_with_recipes, list):
            pairs_with_recipes = [r.strip().lower() for r in s.pairs_with_recipes]

        if isinstance(s.pairs_with_ingredients, str):
            pairs_with_ingredients = [i.strip().lower() for i in s.pairs_with_ingredients.split(",") if i.strip()]
        elif isinstance(s.pairs_with_ingredients, list):
            pairs_with_ingredients = [i.strip().lower() for i in s.pairs_with_ingredients]
        recipe_match = recipe_name.lower() in pairs_with_recipes
        ingredient_match = any(
            ing.name.lower() in pairs_with_ingredients
            for ing in getattr(recipe, "ingredients", [])
        )

        if recipe_match or ingredient_match:
            print(f"✅ Matched spice '{s.name}'")
            suggestions.append({
                "name": s.name,
                "flavor_profile": s.flavor_profile,
                "recommended_quantity": s.recommended_quantity
            })

    spice_session.close()

    print(f"🎯 Final suggestions: {[s['name'] for s in suggestions]}")
    return suggestions