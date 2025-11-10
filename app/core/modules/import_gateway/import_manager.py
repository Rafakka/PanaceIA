"""
import_manager.py

Handles ingestion of external recipe data into PanaceIA's internal schema.
Acts as a 'universal port' for structured recipe imports from crawlers or APIs.

Author: Rafael Kaher
"""

from typing import List, Dict, Any
from app.core.data_cleaner import validate_and_clean_recipe, normalize_universal_input
from app.core.modules.recipes.recipes_manager import add_recipe
from app.core.modules.ingredients.ingredients_manager import add_ingredient


def import_single_recipe(raw_recipe: Dict[str, Any]) -> Dict[str, Any]:
    """
    Import a single recipe object from external structured data.

    Args:
        raw_recipe (dict): The external recipe data. Example:
            {
                "title": "Pancakes",
                "instructions": "Mix and fry.",
                "items": [
                    {"ingredient_name": "Flour", "qty": 200, "measurement": "grams"},
                    {"ingredient_name": "Milk", "qty": 250, "measurement": "mls"}
                ]
            }

    Returns:
        dict: Result of the import process, e.g.:
            {
                "status": "success",
                "imported": "Pancakes",
                "details": { ... cleaned recipe ... }
            }
    """

    # 🔁 Step 1 — Map external keys to PanaceIA schema
    mapped_data = {
        "name": raw_recipe.get("name") or raw_recipe.get("title"),
        "steps": raw_recipe.get("steps") or raw_recipe.get("instructions"),
        "ingredients": []
    }

    for item in raw_recipe.get("ingredients", []) or raw_recipe.get("items", []):
        mapped_data["ingredients"].append({
            "name": item.get("name") or item.get("ingredient_name"),
            "quantity": item.get("quantity") or item.get("qty"),
            "unit": item.get("unit") or item.get("measurement")
        })

    # 🧼 Step 2 — Clean and validate
    cleaned = validate_and_clean_recipe(mapped_data)
    if cleaned["status"] != "success":
        return {"status": "error", "message": "Invalid recipe structure", "details": cleaned}

    # 💾 Step 3 — Persist to DB
    result = add_recipe(cleaned["data"])
    return {
        "status": result.get("status", "error"),
        "imported": mapped_data["name"],
        "message": result.get("message"),
        "details": cleaned["data"]
    }


def import_bulk_recipes(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Import multiple recipes at once from an external data source.

    Args:
        data (list[dict]): List of raw recipe dictionaries.

    Returns:
        dict: Summary of successes and errors.
    """
    successes = []
    errors = []

    for recipe in data:
        result = import_single_recipe(recipe)
        if result["status"] == "success":
            successes.append(result["imported"])
        else:
            errors.append(result)

    return {
        "status": "completed",
        "success_count": len(successes),
        "error_count": len(errors),
        "imported_recipes": successes,
        "failed": errors
    }
