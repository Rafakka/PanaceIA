from fastapi import APIRouter
from app.core.decorators import normalize_input
from app.core.modules.spices.spices_manager import (
    add_spice,
    update_spice,
    list_spices,
    link_spice_to_recipe,
    unlink_spice_from_recipe,
    suggest_spices_for_recipe,
)
from app.core.schemas import SpiceSchema, LinkSpiceSchema
from app.core.modules.spices.utils.spice_bridge import get_recipe_from_main

router = APIRouter(prefix="/spices", tags=["Spices"])


# ============================================================
# 🔹 CREATE
# ============================================================
@router.post("/", status_code=201)
@normalize_input
def add_new_spice(data: SpiceSchema):
    """Create a new spice entry."""
    return add_spice(data.model_dump())

# ============================================================
# 🔹 LIST
# ============================================================
@router.get("/", status_code=200)
def list_all_spices():
    """Return a plain list of spices, not wrapped in {'data': ...}."""
    return list_spices()


# ============================================================
# 🔹 UPDATE
# ============================================================
@router.put("/", status_code=200)
@normalize_input
def update_spice_endpoint(data: SpiceSchema):
    """Update spice attributes."""
    return update_spice(data.model_dump())


# ============================================================
# 🔹 LINK
# ============================================================
@router.post("/link", status_code=201)
@normalize_input
def link_spice(data: LinkSpiceSchema):
    """Link an existing spice to a recipe (bridging recipe from main DB)."""
    recipe = get_recipe_from_main(data.recipe_name)
    if not recipe:
        return {"status": "error", "message": f"Recipe '{data.recipe_name}' not found in main DB."}

    return link_spice_to_recipe(data.recipe_name, data.spice_name)


# ============================================================
# 🔹 UNLINK
# ============================================================
@router.post("/unlink", status_code=200)
@normalize_input
def unlink_spice(data: LinkSpiceSchema):
    """Unlink a spice from a recipe."""
    return unlink_spice_from_recipe(data.recipe_name, data.spice_name)


# ============================================================
# 🔹 SUGGEST
# ============================================================
@router.get("/suggest/{recipe_name}", status_code=200)
def suggest_spices(recipe_name: str):
    """
    Suggest spices based on recipe in main DB.
    Returns a plain list (tests expect a list).
    """
    recipe = get_recipe_from_main(recipe_name)
    if not recipe:
        return {"status": "error", "message": f"Recipe '{recipe_name}' not found."}

    suggestions = suggest_spices_for_recipe(recipe_name)

    if isinstance(suggestions, dict):
        for key in ("suggestions", "data"):
            if key in suggestions:
                return suggestions[key]

        return suggest_spices_for_recipe(recipe_name)

    return suggest_spices_for_recipe(recipe_name)