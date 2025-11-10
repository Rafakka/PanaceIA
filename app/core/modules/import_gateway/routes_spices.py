from fastapi import APIRouter, Body
from app.core.modules.import_gateway.import_manager import import_single_spice, import_bulk_spices

router = APIRouter(prefix="/import", tags=["import"])

@router.post("/spice", status_code=201)
def import_spice_endpoint(spice_data: dict = Body(...)):
    """
    Import a single spice object into PanaceIA.

    Args:
        spice_data (dict): A structured dictionary containing spice data.
            Example:
            {
                "name": "Cinnamon",
                "flavor_profile": "Warm and sweet",
                "recommended_quantity": "1 tsp per loaf",
                "pairs_with_ingredients": ["Banana", "Flour"],
                "pairs_with_recipes": ["Banana Bread"]
            }
    Returns:
        dict: Import status, message, and details.
    """
    return import_single_spice(spice_data)


@router.post("/bulkspices", status_code=201)
def import_bulk_spices_endpoint(payload: list[dict] = Body(...)):
    """
    Import multiple spices at once.

    Args:
        payload (list[dict]): A list of spice dictionaries with the same structure as /spice.

    Returns:
        dict: Summary report containing success and failure counts.
    """
    return import_bulk_spices(payload)