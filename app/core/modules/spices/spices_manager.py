"""
spices_manager.py — Persistent Version

Handles CRUD and suggestion logic for spices.
Integrates with the database via the Spice and RecipeSpice models.
"""

from app.core.db_manager import Recipe, RecipeSpice
from app.core.modules.spices.db.spices_models import SessionLocal, Spice
from app.core.data_cleaner import normalize_string
from collections import Counter

def suggest_spices_for_recipe(recipe_name: str):
    """
    Suggest spices based on stored relationships, with context:
    - flavor_profile
    - recommended_quantity
    """
    session = SessionLocal()
    clean_name = normalize_string(recipe_name)
    try:

        recipe = session.query(Recipe).filter_by(name=clean_name).one_or_none()

        if not recipe:
            session.close()
            return {"status": "error", "message": f"Recipe '{clean_name}' not found."}

        recipe_ingredients = [ri.ingredient.name for ri in recipe.recipe_ingredients]
        all_spices = session.query(Spice).all()

        matches = []
        for spice in all_spices:
            pairs = spice.pairs_with_ingredients.split(",") if spice.pairs_with_ingredients else []
            overlap = len(set(pairs) & set(recipe_ingredients))
            if overlap > 0:
                matches.append({
                    "name": spice.name,
                    "match_score": overlap,
                    "flavor_profile": spice.flavor_profile,
                    "recommended_quantity": spice.recommended_quantity
                })

        session.close()
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return {"status": "success", "suggestions": matches}
    except Exception:
        return {"status": "error", "message": "Database not initialized"}

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
    data = [{"name": s.name, "flavor_profile": s.flavor_profile} for s in spices]
    session.close()
    return {"status": "success", "data": data}


def link_spice_to_recipe(recipe_name: str, spice_name: str):
    """Link an existing spice to a recipe and learn from it."""
    session = SessionLocal()
    clean_recipe = normalize_string(recipe_name)
    clean_spice = normalize_string(spice_name)

    recipe = session.query(Recipe).filter_by(name=clean_recipe).one_or_none()
    spice = session.query(Spice).filter_by(name=clean_spice).one_or_none()

    if not recipe or not spice:
        session.close()
        return {"status": "error", "message": "Recipe or spice not found."}

    existing = (
        session.query(RecipeSpice)
        .filter_by(recipe_id=recipe.id, spice_id=spice.id)
        .one_or_none()
    )
    if existing:
        session.close()
        return {"status": "error", "message": f"'{spice.name}' already linked to '{recipe.name}'."}

    link = RecipeSpice(recipe=recipe, spice=spice)
    session.add(link)

    recipes_known = set(spice.pairs_with_recipes.split(",")) if spice.pairs_with_recipes else set()
    recipes_known.add(recipe.name)
    spice.pairs_with_recipes = ",".join(recipes_known)

    session.commit()
    session.close()
    return {"status": "success", "message": f"'{spice.name}' linked to '{recipe.name}' and learned from it."}


def unlink_spice_from_recipe(recipe_name: str, spice_name: str):
    """Remove a spice from a recipe."""
    session = SessionLocal()
    clean_recipe = normalize_string(recipe_name)
    clean_spice = normalize_string(spice_name)

    recipe = session.query(Recipe).filter_by(name=clean_recipe).one_or_none()
    spice = session.query(Spice).filter_by(name=clean_spice).one_or_none()

    if not recipe or not spice:
        session.close()
        return {"status": "error", "message": "Recipe or spice not found."}

    link = (
        session.query(RecipeSpice)
        .filter_by(recipe_id=recipe.id, spice_id=spice.id)
        .one_or_none()
    )
    if not link:
        session.close()
        return {"status": "error", "message": f"'{spice.name}' not linked to '{recipe.name}'."}

    session.delete(link)
    session.commit()
    session.close()
    return {"status": "success", "message": f"'{spice.name}' unlinked from '{recipe.name}'."}

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