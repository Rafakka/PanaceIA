"""
spices_manager.py — Persistent Version

Handles CRUD and suggestion logic for spices.
Integrates with the database via the Spice and RecipeSpice models.
"""

from app.core.db_manager import SessionLocal, Recipe, Spice, RecipeSpice
from app.core.data_cleaner import normalize_string
from collections import Counter

SPICE_LIBRARY = {
    "Garlic": ["Tomato", "Beef", "Pasta"],
    "Cumin": ["Chickpeas", "Beans", "Rice"],
    "Paprika": ["Chicken", "Potato", "Egg"],
    "Turmeric": ["Rice", "Lentils", "Coconut Milk"],
    "Cinnamon": ["Apple", "Oats", "Pumpkin"],
    "Basil": ["Tomato", "Pasta", "Mozzarella"]
}

def suggest_spices_for_recipe(recipe_name: str):
    """Suggest spices based on existing ingredients."""
    session = SessionLocal()
    clean_name = normalize_string(recipe_name)
    recipe = session.query(Recipe).filter_by(name=clean_name).one_or_none()

    if not recipe:
        session.close()
        return {"status": "error", "message": f"Recipe '{clean_name}' not found."}

    recipe_ingredients = [ri.ingredient.name for ri in recipe.recipe_ingredients]

    scores = Counter()
    for spice, pairs in SPICE_LIBRARY.items():
        for ingredient in recipe_ingredients:
            if ingredient in pairs:
                scores[spice] += 1

    ranked = [s for s, _ in scores.most_common()]
    session.close()
    return {"status": "success", "data": ranked}


def add_spice(spice_name: str, flavor_profile: str = None):
    """Add a spice to the database (if it doesn’t exist)."""
    session = SessionLocal()
    spice_name = normalize_string(spice_name)

    existing = session.query(Spice).filter_by(name=spice_name).one_or_none()
    if existing:
        session.close()
        return {"status": "error", "message": f"'{spice_name}' already exists."}

    spice = Spice(name=spice_name, flavor_profile=flavor_profile)
    session.add(spice)
    session.commit()
    session.close()
    return {"status": "success", "message": f"'{spice_name}' added."}


def list_spices():
    """List all spices in the database."""
    session = SessionLocal()
    spices = session.query(Spice).all()
    data = [{"name": s.name, "flavor_profile": s.flavor_profile} for s in spices]
    session.close()
    return {"status": "success", "data": data}


def link_spice_to_recipe(recipe_name: str, spice_name: str):
    """Link an existing spice to a recipe."""
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
    session.commit()
    session.close()
    return {"status": "success", "message": f"'{spice.name}' linked to '{recipe.name}'."}


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
