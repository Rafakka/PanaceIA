from typing import List, Dict, Any
from app.core.modules.spices.spices_manager import add_spice
from app.core.data_cleaner import normalize_universal_input
from app.core.modules.spices.utils import link_spice_to_recipe, suggest_spices_for_recipe


def import_single_spice(raw_spice: Dict[str, Any]) -> Dict[str, Any]:

    mapped_data = {
        "name": raw_spice.get("name") or raw_spice.get("title"),
        "flavor_profile": raw_spice.get("flavor") or raw_spice.get("taste"),
        "recommended_quantity": raw_spice.get("recommended_quantity") or raw_spice.get("dosage"),
        "pairs_with_ingredients": raw_spice.get("combines_ingredients") or raw_spice.get("pairings_ingredients"),
        "pairs_with_recipes": raw_spice.get("recipes") or raw_spice.get("pairings_recipes")
    }

    for key in ("pairs_with_ingredients", "pairs_with_recipes"):
        val = mapped_data.get(key)
        if isinstance(val, str):
            mapped_data[key] = [v.strip() for v in val.split(",")]

    cleaned = normalize_universal_input(mapped_data)

    result = add_spice(cleaned)

    for recipe_name in mapped_data.get ("pairs_with_recipes") or []:
        link_spice_to_recipe(mapped_data["name"], recipe_name)
        
    for suggest_recipe_name in mapped_data.get ("pairs_with_recipes") or []:
        suggest_spices_for_recipe(suggest_recipe_name)

    return {
        "status": result.get("status", "error"),
        "imported": mapped_data["name"],
        "message": result.get("message"),
        "details": cleaned
    }


def import_bulk_spices(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Import multiple spices at once.
    """
    successes = []
    errors = []

    for spice in data:
        result = import_single_spice(spice)
        if result["status"] == "success":
            successes.append(result["imported"])
        else:
            errors.append(result)

    return {
        "status": "completed",
        "success_count": len(successes),
        "error_count": len(errors),
        "imported_spices": successes,
        "failed": errors
    }
