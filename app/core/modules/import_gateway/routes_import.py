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
    """
    Import a single spice entry from an external source.
    """

    cleaned = import_single_spice(spice)

    if cleaned["status"] == "error":
        return cleaned

    data = cleaned["data"]

    db_result = add_spice(data)

    if db_result.get("status") == "success":
        return {
            "status": "success",
            "name": data.get("name"),
            "message": db_result.get("message", "Spice imported successfully.")
        }
    else:
        return {
            "status": "error",
            "name": data.get("name"),
            "message": db_result.get("message", "Failed to insert spice.")
        }

@router.post("/bulkspices", status_code=201)
def import_bulk_spices_endpoint(spices: list[dict] = Body(...)):
    """
    Import multiple spices in bulk, each validated through the importer.
    """
    normalized_results = import_bulk_spices(spices)

    final_results = []

    for item in normalized_results:
        if item["status"] == "error":
            final_results.append(item)
            continue

        data = item["data"]

        db_result = add_spice(data)

        if db_result.get("status") == "success":
            final_results.append({
                "status": "success",
                "name": data.get("name"),
                "message": db_result.get("message", "Spice imported successfully.")
            })
        else:
            final_results.append({
                "status": "error",
                "name": data.get("name"),
                "message": db_result.get("message", "Failed to insert spice.")
            })
    return final_results
