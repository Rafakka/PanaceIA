"""
routes_spices.py
"""

from fastapi import APIRouter, Body
from app.core.modules.spices.spices_manager import (
    suggest_spices_for_recipe,
    add_spice,
    list_spices,
    link_spice_to_recipe,
    unlink_spice_from_recipe
)
from app.core.modules.spices.spices_manager import update_spice
from app.core.decorators import normalize_input
from app.core.schemas import SpiceSchema, LinkSpiceSchema

router = APIRouter(prefix="/spices", tags=["spices"])

@router.get("/")
def list_all_spices():
    """List all available spices."""
    return list_spices()

@router.get("/suggest/{recipe_name}")
@normalize_input
def suggest_spices(recipe_name: str):
    """Suggest spices based on a recipe’s ingredients."""
    return suggest_spices_for_recipe(recipe_name)

@router.post("/", status_code=201)
@normalize_input
def add_new_spice(data:SpiceSchema):
    """Add a new spice to the library."""
    return add_spice(data)

@router.post("/link", status_code=201)
@normalize_input
def link_spice(data: LinkSpiceSchema):
    """Link an existing spice to a recipe."""
    return link_spice_to_recipe(
        data.spice_name,
        data.recipe_name
    )

@router.put("/", status_code=200)
@normalize_input
def update_spice_endpoint(data: SpiceSchema):
    """Update spice details (flavor, recommended quantity, or associations)."""
    return update_spice(data)

@router.delete("/unlink", status_code=200)
@normalize_input
def unlink_spice(data: SpiceSchema):
    """Remove a spice from a recipe."""
    return unlink_spice_from_recipe(
        data.spice_name,
        data.recipe_name
    )