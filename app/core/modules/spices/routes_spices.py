"""
routes_spices.py — Persistent Version
"""

from fastapi import APIRouter, Body
from app.core.modules.spices.spices_manager import (
    suggest_spices_for_recipe,
    add_spice,
    list_spices,
    link_spice_to_recipe,
    unlink_spice_from_recipe
)

router = APIRouter(prefix="/spices", tags=["spices"])

@router.get("/")
def list_all_spices():
    """List all available spices."""
    return list_spices()

@router.get("/suggest/{recipe_name}")
def suggest_spices(recipe_name: str):
    """Suggest spices based on a recipe’s ingredients."""
    return suggest_spices_for_recipe(recipe_name)

@router.post("/", status_code=201)
def add_new_spice(data: dict = Body(...)):
    """Add a new spice to the library."""
    return add_spice(data["name"], data.get("flavor_profile"))

@router.post("/link", status_code=201)
def link_spice(data: dict = Body(...)):
    """Link an existing spice to a recipe."""
    return link_spice_to_recipe(data["recipe_name"], data["spice_name"])

@router.delete("/unlink", status_code=200)
def unlink_spice(data: dict = Body(...)):
    """Remove a spice from a recipe."""
    return unlink_spice_from_recipe(data["recipe_name"], data["spice_name"])
