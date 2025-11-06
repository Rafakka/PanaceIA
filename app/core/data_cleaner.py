"""
data_cleaner.py

Provides all normalization, cleaning, and validation utilities 
for ensuring consistent and standardized data across the system.

This module sanitizes input data before it reaches the business logic layer,
handling normalization of strings, quantities, and measurement units.
It also validates schema integrity using Pydantic models.

Author: Rafael Kaher
"""

from app.core.schemas import IngredientSchema, RecipeSchema
from pydantic import ValidationError

def normalize_string(value:str | dict) ->str|dict:
    """
    Normalize string or dict values by trimming whitespace and applying title casing.

    Args:
        value (str): The string to be normalized.
        value (dict): The dict to be normalized.

    Returns:
        str: The cleaned string if valid, otherwise returns the original value.
        dict: The cleaned dict if valid, otherwise returns none.

    Example:
        ```python
        normalize_string("  panCAke mix  ")
        # Returns: 'Pancake Mix'
        ```
    """
    if isinstance(value, dict):
        cleaned_dict = {
            key.strip().title(): v.strip().title() if isinstance(v, str) else v
            for key, v in value.items()
        }
        return cleaned_dict  

    return value.strip().title() if isinstance(value,str) else value

def normalize_quantity(value: float | dict) -> float|dict:
    """
    Convert quantity values to floats when possible.

    Args:
        value (any): A numeric/tring or a dict value representing quantity.

    Returns:
        dict | float | None: The converted float value, dict or None if conversion fails.
        

    Example:
        ```python
        normalize_quantity("200")
        # Returns: 200.0
        ```
    """
    if isinstance(value, dict):
        cleaned_dict = {}
        for key, v in value.items():
            clean_key = key.strip().title() if isinstance(key, str) else key
            try:
                clean_value = float(v)
            except (ValueError, TypeError):
                clean_value = v
            cleaned_dict[clean_key] = clean_value
        return cleaned_dict
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def normalize_unit(value: str | dict) -> str | dict:
    """
    Normalize units of measurement into standardized abbreviations.

    Args:
        value (str): A string representing a measurement unit.
        value (dict): A dict with values representing a measurement unit.

    Returns:
        str: The standardized unit if found in the unit map, otherwise the input itself.
        dict: The standardized unito if found in unit map, othewise the input itself.
    Example:
        ```python
        normalize_unit("gramas")
        # Returns: 'Grm'
        ```
    """
    unit_map = {
        "gramas":"Grm",
        "gramos":"Grm",
        "gram":"Grm",
        "gms":"Grm",
        "mls":"Mls",
        "mililitros":"Mls",
        "cps":"Cps",
        "copos":"Cps",
        "copo":"Cp",
        "colher":"Cl",
        "colheres":"Cls",
        "colheres de sopa":"Cls Sopa",
        "colher de sopa":"Cl Sopa",
        "colher de sobremesa":"Cl SobreMs",
        "colheres de sobremesa":"Cls SobreMs",
        "colheres de cha":"Cls Chá",
        "colher de cha":"Cl Chá",
        "xicara":"Xca",
        "xicaras":"Xcas",
        "chicara":"Xca",
        "chicaras":"Xcas",
        "kilos":"Kgs",
        "kilo":"Kg",
        "quilo":"Kg",
        "quilos":"Kgs",
        "unit":"Unit"
    }
    if isinstance(value, dict):
        cleaned_dict = {}
        for key, v in value.items():
            clean_key = key.strip().title() if isinstance(key, str) else key
            if isinstance(v, str):
                raw_value = v.strip().lower()
                clean_value = unit_map.get(raw_value, v.title())
            else:
                clean_value = v
            cleaned_dict[clean_key] = clean_value
        return cleaned_dict
    try:
        v = value.strip().lower()
        return unit_map.get(v, value.strip())
    except (ValueError, TypeError):
        return None

def clean_recipe(data: dict) -> dict:
    """
    Clean and normalize a recipe dictionary, including nested ingredients.

    Args:
        data (dict): Must include:
            - `name` (str)
            - `steps` (str)
            - `ingredients` (list[dict])

    Returns:
        dict: A fully cleaned recipe dictionary.

    Example:
        ```python
        clean_recipe({
            "name": "Pancakes",
            "steps": "mix ingredients and fry until golden",
            "ingredients": [
                {"name": "flour", "quantity": "200", "unit": "gramas"},
                {"name": "milk", "quantity": "250", "unit": "mls"}
            ]
        })
        # Returns cleaned name, steps, and ingredients
        ```
    """
    return {
        "name": normalize_string(data.get("name")),
        "steps": normalize_string(data.get("steps")),
        "ingredients": [
            apply_cleaning(i, {
                "name": normalize_string,
                "quantity": normalize_quantity,
                "unit": normalize_unit
            }) for i in data.get("ingredients", [])
        ]
    }

def apply_cleaning(data: dict, cleaning_map: dict):
    """
    Apply normalization functions to each key-value pair in a dictionary.

    Args:
        data (dict): The input dictionary to be cleaned.
        cleaning_map (dict[str, callable]): A mapping of field names to their cleaning functions.

    Returns:
        dict: A new dictionary with cleaned key-value pairs.

    Example:
        ```python
        apply_cleaning(
            {"name": "flour", "quantity": "200", "unit": "gramas"},
            {"name": normalize_string, "quantity": normalize_quantity, "unit": normalize_unit}
        )
        # Returns: {'name': 'Flour', 'quantity': 200.0, 'unit': 'Grm'}
        ```
    """
    return {
        key: cleaning_map[key](value)
        for key, value in data.items()
        if key in cleaning_map and value is not None
    }

def validate_and_clean_ingredient(raw_data: dict):
    """
    Validate and clean a raw ingredient dictionary.

    Args:
        raw_data (dict): Must contain:
            - `name` (str)
            - `quantity` (float or str)
            - `unit` (str)

    Returns:
        dict: A response dictionary with status and cleaned data.

    Example:
        ```python
        validate_and_clean_ingredient({
            "name": "milk", "quantity": "250", "unit": "ml"
        })
        # Returns: {"status": "success", "data": {"name": "Milk", "quantity": 250.0, "unit": "Ml"}}
        ```
    """
    normalized = apply_cleaning(
        raw_data,
        {"name": normalize_string, "quantity": normalize_quantity, "unit": normalize_unit}
    )
    try:
        valid = IngredientSchema(**normalized)
    except ValidationError as e:
        return {"status": "error", "message": e.errors()}

    return {"status": "success", "data": normalized}

def validate_and_clean_recipe(raw_data: dict):
    """
    Validate and clean a raw recipe dictionary, including nested ingredients.

    Args:
        raw_data (dict): Must contain:
            - `name` (str)
            - `steps` (str)
            - `ingredients` (list[dict])

    Returns:
        dict: A response dictionary with status and cleaned data.

    Example:
        ```python
        validate_and_clean_recipe({
            "name": "Pancakes",
            "steps": "Mix ingredients and fry until golden.",
            "ingredients": [
                {"name": "Flour", "quantity": 200, "unit": "Grm"},
                {"name": "Milk", "quantity": 250, "unit": "Mls"}
            ]
        })
        # Returns: {"status": "success", "data": { ... cleaned recipe ... }}
        ```
    """
    normalized = clean_recipe(raw_data)
    try:
        valid = RecipeSchema(**normalized)
    except ValidationError as e:
        return {"status": "error", "message": e.errors()}
    return {"status": "success", "data": clean_recipe(valid.model_dump())}

def normalize_universal_input(value):
    available_cleaners = {
        fn.split("normalize_")[1]: func
        for fn, func in globals().items()
        if fn.startswith("normalize_") and callable(func)
    }

    approved_tokens = {"name", "quantity", "unit"}

    token_aliases = {
        "name": "string",
        "quantity": "quantity",
        "unit": "unit",
        "steps":"string",
        "ingredient":"string"
    }

    excluded_fields = {"username", "hostname", "email"}

    if isinstance(value, dict):
        clean_dict = {}

        for key, v in value.items():
            normalized_key = key.strip().lower() if isinstance(key, str) else key
            cleaned = False

            if normalized_key in excluded_fields:
                clean_dict[key] = v
                continue

            for semantic_token, actual_token in token_aliases.items():
                cleaner_func = available_cleaners.get(actual_token)

                if not cleaner_func or semantic_token not in approved_tokens:
                    continue

                if (
                    normalized_key == semantic_token
                    or f"_{semantic_token}" in normalized_key
                    or normalized_key.endswith(semantic_token)
                ):
                    try:
                        clean_dict[key] = cleaner_func(v)
                        cleaned = True
                        break
                    except Exception:
                        clean_dict[key] = v
                        cleaned = True
                        break

            if not cleaned:
                clean_dict[key] = v

        return clean_dict

    
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.replace(".", "", 1).isdigit():
            return normalize_quantity(stripped)
        return normalize_string(value)
    elif isinstance(value, (int, float)):
        return normalize_quantity(value)
    else:
        return value
