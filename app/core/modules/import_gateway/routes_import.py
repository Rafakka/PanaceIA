from fastapi import APIRouter, Body
from app.core.modules.import_gateway.import_manager import import_single_recipe, import_bulk_recipes
from app.core.modules.spices.spices_manager import add_spice
from app.core.modules.import_gateway.spices_manager import import_bulk_spices, import_single_spice

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/recipe", status_code=201)
def import_recipe_endpoint(recipe_data: dict = Body(...)):
    """Import a single recipe object into PanaceIA."""
    return import_single_recipe(recipe_data)

@router.post("/bulk", status_code=201)
def import_bulk_endpoint(payload: list[dict] = Body(...)):
    """Import multiple recipes at once."""
    return import_bulk_recipes(payload)

@router.post("/spice", status_code=201)
def import_single_spice_endpoint(spice: dict = Body(...)):
    cleaned = import_single_spice(spice)
    if cleaned["status"] == "error":
        return cleaned
        
    data = cleaned["data"]
    result = add_spice(data)
    return {"status": "success", "message": result.get("message", "Spice imported successfully.")}

@router.post("/bulkspices", status_code=201)
def import_bulk_spices_endpoint(spices: list[dict] = Body(...)):
    """
    Import multiple spices in bulk.
    """
    results = []
    for item in spices:
        cleaned = import_single_spice(item)
        if cleaned["status"] == "error":
            results.append(cleaned)
            continue

        data = cleaned["data"]
        added = add_spice(data)
        results.append({"status": "success", "message": added.get("message", "Spice imported successfully.")})

    return results
