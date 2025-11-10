from fastapi import APIRouter, Body
from app.core.modules.import_gateway.import_manager import import_single_recipe, import_bulk_recipes

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/recipe", status_code=201)
def import_recipe_endpoint(recipe_data: dict = Body(...)):
    """Import a single recipe object into PanaceIA."""
    return import_single_recipe(recipe_data)

@router.post("/bulk", status_code=201)
def import_bulk_endpoint(payload: list[dict] = Body(...)):
    """Import multiple recipes at once."""
    return import_bulk_recipes(payload)
