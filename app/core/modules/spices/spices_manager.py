"""
spices_manager.py — Persistent Version

Handles CRUD and suggestion logic for spices.
Integrates with the database via the Spice and RecipeSpice models.
"""

from app.core.db_manager import Recipe, RecipeSpice
from app.core.modules.spices.db.spices_models import SessionLocal, Spice
from app.core.data_cleaner import normalize_string
from collections import Counter
from app.core.modules.spices.utils.spice_bridge import link_spice_to_recipe as bridge_link_spice_to_recipe
from app.core.modules.spices.utils.spice_bridge import unlink_spice_from_recipe as bridge_unlink_spice_from_recipe
from app.core.modules.spices.utils.spice_bridge import suggest_spices_for_recipe as bridge_suggest_spices_for_recipe

def suggest_spices_for_recipe(recipe_name: str):
    """
    Suggest spices that pair well with a recipe.
    Delegates to the cross-database bridge.
    """
    result = bridge_suggest_spices_for_recipe(recipe_name)
    return result

def add_spice(spice_data: dict):
    """
        Add a spice with extended attributes:
        - flavor_profile: short text describing its taste
        - recommended_quantity: e.g. "1 tsp per 500g meat"
        - pairs_with_ingredients: comma-separated list (stored as text)
        - pairs_with_recipes: comma-separated list (optional)
    """
    session = SessionLocal()

    if not isinstance(spice_data, dict):
        spice_data = spice_data.model_dump()

    name = normalize_string(spice_data.get("name"))

    existing = session.query(Spice).filter_by(name=name).one_or_none()
    if existing:
        session.close()
        return {"status": "error", "message": f"Spice '{name}' already exists."}

    flavor_profile = spice_data.get("flavor_profile", "")
    recommended_quantity = spice_data.get("recommended_quantity", "")
    pairs_with_ingredients = ",".join(spice_data.get("pairs_with_ingredients", []))
    pairs_with_recipes = ",".join(spice_data.get("pairs_with_recipes", []))

    spice = Spice(
        name=name,
        flavor_profile=flavor_profile,
        recommended_quantity=recommended_quantity,
        pairs_with_ingredients=pairs_with_ingredients,
        pairs_with_recipes=pairs_with_recipes
    )
    session.add(spice)
    session.commit()
    session.close()
    return {"status": "success", "message": f"Spice '{name}' added with full context."}


def list_spices():
    """List all spices in the database."""
    session = SessionLocal()
    spices = session.query(Spice).all()
    session.close()

    result = []
    for s in spices:
        spice_dict = {k: v for k, v in vars(s).items() if not k.startswith("_")}
        result.append(spice_dict)
    return result

def link_spice_to_recipe(recipe_name: str, spice_name: str):
    """
    Link an existing spice to a recipe and learn from it.
    Delegates to the cross-database bridge to ensure both
    recipe and spice are validated across their databases.
    """
    result = bridge_link_spice_to_recipe(spice_name, recipe_name)

    if result.get("status") == "success":
        return {"status": "success", "message": result.get("message", "Linked successfully.")}
    return {"status": "error", "message": result.get("message", "Link failed.")}

def unlink_spice_from_recipe(recipe_name: str, spice_name: str):
    """
    Unlink an existing spice from a recipe across databases.
    Delegates to the cross-database bridge.
    """
    result = bridge_unlink_spice_from_recipe(spice_name=spice_name, recipe_name=recipe_name)

    if result.get("status") == "success":
        return {"status": "success", "message": result.get("message", "Unlinked successfully.")}
    return {"status": "error", "message": result.get("message", "Unlink failed.")}

def update_spice(spice_data: dict):
    """
    Update an existing spice's details.
    You can update its flavor profile, recommended quantity,
    or add new compatible ingredients and recipes.
    """
    session = SessionLocal()

    if not isinstance(spice_data, dict):
        spice_data = spice_data.model_dump()

    name = normalize_string(spice_data.get("name"))
    spice = session.query(Spice).filter_by(name=name).one_or_none()
    if not spice:
        session.close()
        return {"status": "error", "message": f"Spice '{name}' not found."}

    if "flavor_profile" in spice_data:
        spice.flavor_profile = spice_data["flavor_profile"]
    if "recommended_quantity" in spice_data:
        spice.recommended_quantity = spice_data["recommended_quantity"]

    if "pairs_with_ingredients" in spice_data:
        new_ings = set(spice.pairs_with_ingredients.split(",")) | set(spice_data["pairs_with_ingredients"])
        spice.pairs_with_ingredients = ",".join(filter(None, new_ings))

    if "pairs_with_recipes" in spice_data:
        new_recs = set(spice.pairs_with_recipes.split(",")) | set(spice_data["pairs_with_recipes"])
        spice.pairs_with_recipes = ",".join(filter(None, new_recs))

    session.commit()
    session.close()
    return {"status": "success", "message": f"Spice '{name}' updated successfully."}

def auto_learn_from_recipe(recipe_name: str):
    """
    Learn new spice-ingredient associations automatically from the recipe content.
    This is PanaceIA's 'rudimentary AI' mechanism.
    """
    session = SessionLocal()
    clean_name = normalize_string(recipe_name)
    recipe = session.query(Recipe).filter_by(name=clean_name).one_or_none()
    if not recipe:
        session.close()
        return

    recipe_ingredients = [ri.ingredient.name for ri in recipe.recipe_ingredients]
    spices_linked = [link.spice for link in recipe.spice_links]

    for spice in spices_linked:
        existing_pairs = set(spice.pairs_with_ingredients.split(",")) if spice.pairs_with_ingredients else set()
        new_pairs = set(recipe_ingredients)
        spice.pairs_with_ingredients = ",".join(existing_pairs | new_pairs)
    session.commit()
    session.close()