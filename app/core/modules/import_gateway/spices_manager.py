from typing import List, Dict, Any
from app.core.modules.spices.spices_manager import add_spice
from app.core.data_cleaner import normalize_universal_input
from app.core.modules.spices.utils.spice_bridge import link_spice_to_recipe, suggest_spices_for_recipe
from typing import Dict, Any
from app.core.utils.data_cleaner import normalize_universal_input

def import_single_spice(raw_spice: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize and validate a single spice payload.

    Returns:
        dict: {"status": "success", "data": {...}} or {"status": "error", "message": "..."}
    """

    if not isinstance(raw_spice, dict):
        return {"status": "error", "message": "Invalid spice structure"}

    mapped_data = {
        "name": raw_spice.get("name") or raw_spice.get("title"),
        "flavor_profile": raw_spice.get("flavor_profile") or raw_spice.get("flavor") or raw_spice.get("taste"),
        "recommended_quantity": raw_spice.get("recommended_quantity") or raw_spice.get("dosage"),
        "pairs_with_ingredients": (
            raw_spice.get("pairs_with_ingredients") 
            or raw_spice.get("combines_ingredients") 
            or raw_spice.get("pairings_ingredients")
        ),
        "pairs_with_recipes": (
            raw_spice.get("pairs_with_recipes") 
            or raw_spice.get("recipes") 
            or raw_spice.get("pairings_recipes")
        )
    }

    if not mapped_data.get("name"):
        return {"status": "error", "message": "Missing required field: name"}

    for key in ("pairs_with_ingredients", "pairs_with_recipes"):
        val = mapped_data.get(key)
        if isinstance(val, str):
            mapped_data[key] = [v.strip() for v in val.split(",") if v.strip()]

    if not isinstance(mapped_data.get("pairs_with_ingredients"), list):
        mapped_data["pairs_with_ingredients"] = []
    if not isinstance(mapped_data.get("pairs_with_recipes"), list):
        mapped_data["pairs_with_recipes"] = []

    cleaned = normalize_universal_input(mapped_data)
    return {"status": "success", "data": cleaned}

def import_bulk_spices(spices: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Import multiple spices at once.
    """
    results = []

    for spice in spices:
        result = import_single_spice(spice)
        results.append(result)

    return results