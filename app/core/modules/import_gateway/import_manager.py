"""
PanaceIA Import Gateway
=======================

Handles ingestion, validation, and normalization of external recipe or spice data.
Outputs API-like responses for smooth integration with other modules.
"""

from typing import List, Dict, Any
from app.core.data_cleaner import validate_and_clean_recipe

# ---------------------------------------------------------------------------
# 🔹 Single Importer
# ---------------------------------------------------------------------------

def import_single_recipe(raw_recipe: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize and validate a single recipe payload.

    Returns:
        dict: {"status": "success", "data": {...}} or {"status": "error", "message": "..."}
    """

    if not isinstance(raw_recipe, dict):
        return {"status":"error", "message":"Invalid recipe structure"}

    name = raw_recipe.get ("name","")
    steps = raw_recipe.get ("steps","")
    ingredients = raw_recipe.get ("ingredients",[])

    if not name or not steps or not isinstance(ingredients, list):
        return {"status":"error", "message":"Invalid recipe structure"}

    for ing in ingredients:
        q = str(ing.get("quantity", "")).strip()
        if not q:
            return {"status":"error", "message": f"Invalid quantity for ingredient '{ing.get('name','?')}'"}
        try:
            _ = float(q)
        except ValueError:
            return {"status":"error", "message": f"Invalid quantity for ingredient '{ing.get('name','?')}'"}
    
    try:
        from app.core.data_cleaner import normalize_universal_input
        cleaned = normalize_universal_input(raw_recipe)
    except Exception as e:
        return {"status": "error", "message": f"Normalization failed: {e}"}

    for ing in cleaned.get("ingredients", []):
        ing["quantity"] = float(ing["quantity"])

    return {"status":"success", "data": cleaned}

# ---------------------------------------------------------------------------
# 🔹 Bulk Importer
# ---------------------------------------------------------------------------

def import_bulk_recipes(list_of_raws: list[dict]) -> list[dict]:
    """
    Normalize multiple recipes, keeping individual status per recipe.

    Args:
        data (list[dict]): List of raw recipe dictionaries.

    Returns:
        list[dict]: Each item contains {"status": ..., "data" or "message": ...}
    """
    results = []
    for item in list_of_raws:
        results.append(import_single_recipe(item))
    return results