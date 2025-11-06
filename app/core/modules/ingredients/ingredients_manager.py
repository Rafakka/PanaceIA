"""
ingredients_manager.py

Handles all CRUD operations and logic related to ingredients only.
Each function here communicates directly with the database through SQLAlchemy ORM
and uses the data_cleaner module for safe input normalization.

All functions return structured dictionaries that can be serialized to JSON
and consumed directly by FastAPI routes.

Author: Rafael Kaher
"""

from app.core.data_cleaner import normalize_universal_input
from app.core import db_manager
from app.core.db_manager import Ingredient, RecipeIngredient

def add_ingredient(ingredient_data: dict):
    """
    Add an ingredient to the data base.
    
    Args:
        recipe_data (dict): A dictionary containing:
                - name (str): Ingredient's name.
                - unit (str): Measurement's unit.
                - quantity (float): Ingredient's numerical quantity.

    Returns:
        dict: A status message indicating success or failure.
    
    Example:
        ```python
        add_ingredient({
            "name": "Eggs",
            "unit": "Unit.",
            "quantity":"2.0"
        })
        ```
    """
    session = db_manager.SessionLocal()

    clean_ingredient = normalize_universal_input(ingredient_data)
    name = clean_ingredient["name"]
    unit = clean_ingredient["unit"]

    existing = session.query(Ingredient).filter_by(name=name).first()
    if existing:
        session.close()
        return {"status": "error", "message": f"Ingredient '{name}' already exists."}

    try:
        ingredient = Ingredient(name=name, unit=unit)
        session.add(ingredient)
        session.commit()
        session.close()
        return {"status": "success", "name": name, "unit": unit}
    except Exception as e:
        session.rollback()
        session.close()
        return {"status": "error", "message": str(e)}

def list_ingredients():
    """
    Retrieve all ingredients from the database.

    Returns:
        dict: Contains:
            - status (str): "success" or "error".
            - data (list[dict]): Each recipe includes:
                - name (str)
                - quantity (float)
                - unit (str)

    Example:
        ```python
        list_ingredients()
        # -> {"status": "success", "data": [{"name": "Flour", "quantity": "100.0", "unit":"Mg"}]}
        ```
    """
    session = db_manager.SessionLocal()
    ingredients = session.query(Ingredient).all()
    result = [
        {"name": i.name, "unit": i.unit}
        for i in ingredients
    ]
    session.close()
    return result

def get_ingredient_name(value: str | dict) -> dict:
    """
    Retrieve an ingredient by name.

    Args:
        value (str | dict): Ingredient name (e.g., "eggs") or dict containing {"name": "eggs"}.

    Returns:
        dict: Contains:
            - status (str): "success" or "error".
            - data (dict): Ingredient details if found.
            - message (str): Error message if not found.

    Example:
        ```python
        get_ingredient_name("eggs")
        # -> {"status": "success", "data": {"name": "Eggs", "unit": "Unit"}}
        ```
    """
    session = db_manager.SessionLocal()

    if isinstance(value, dict):
        raw_name = value.get("name")
    else:
        raw_name = value

    name = normalize_universal_input(raw_name)

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()

    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    data = {"name": ingredient.name, "unit": ingredient.unit}

    session.close()
    return {"status": "success", "data": data}

def update_ingredient_name(ingredient_data: dict):
    """
    Updates a ingredient's name.
    
    Args:
        recipe_data (dict): A dictionary containing:
                - old_name (str): Ingredient's name.
                - new_name (str): Measurement's unit.
    
    Returns:
        dict: A message indicating whether the update succeeded.
    
    Example:
        ```python
        update_ingredient_name({
            "old_name": "Pancakes",
            "new_name": "Fluffy Pancakes"
        })
        ```
    """
    session = db_manager.SessionLocal()

    if not isinstance(ingredient_data, dict):
        ingredient_data = ingredient_data.model_dump()
    
    clean_data = normalize_universal_input(ingredient_data)
    old_name = clean_data["old_name"]
    new_name = clean_data["new_name"]

    existing = session.query(Ingredient).filter_by(name=new_name).first()
    if existing:
        session.close()
        return {"status": "error", "message": f"Ingredient '{new_name}' already exists."}

    ingredient = session.query(Ingredient).filter_by(name=old_name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{old_name}' not found."}

    ingredient.name = new_name

    try:
        session.commit()
        session.close()
        return {"status": "success", "updated": old_name, "new_name": new_name}
    except Exception as e:
        session.rollback()
        session.close()
        return {"status": "error", "message": str(e)}


def update_ingredient_quantity(ingredient_data: dict):
    """
    Updates a ingredient's quantity.
    
    Args:
        recipe_data (dict): A dictionary containing:
                - name(str) : Ingredient's name.
                - new_quantity (float): Decimal number of quantity.
    Returns:
        dict: A message indicating whether the update succeeded, with old ingredient's name and new ingredient's name.
    
    Example:
        ```python
        update_ingredient_quantity({
            "name": "Rice",
            "new_quantity": "125.0"
        })
        ```
    """

    session = db_manager.SessionLocal()

    if not isinstance(ingredient_data, dict):
        ingredient_data = ingredient_data.model_dump()

    clean_ingredient = normalize_universal_input(ingredient_data)

    name = clean_ingredient["name"]
    new_quantity = clean_ingredient["new_quantity"]

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}
    ingredient.quantity = new_quantity
    session.commit()
    session.close()
    return {"status": "success", "ingredient": name, "new_quantity": new_quantity}

def update_ingredient_unit(ingredient_data: dict):
    """
    Change ingredients unit's measure.
    
    Args:
        update_data (dict): a dictionary containing:
            - name (str) : Ingredient's name.
            - new_unit (str) : New's unit measure.
    
    Returns:
        dict: A message indicating whether the update succeeded, with old ingredient's name and new ingredient's unit.
    
    Example:
        ```python
        update_ingredients_unit({
            "name": "eggs",
            "new_unit: "grams"
        })
        ```
    """
    session = db_manager.SessionLocal()
    
    if not isinstance(ingredient_data, dict):
        ingredient_data = ingredient_data.model_dump()

    clean_ingredient = normalize_universal_input(ingredient_data)

    name = clean_ingredient["name"]
    new_unit = clean_ingredient["new_unit"]

    name = ingredient_data.get("name")
    new_unit = ingredient_data.get("new_unit")

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    ingredient.unit = new_unit
    session.commit()
    session.close()
    return {"status": "success", "ingredient": name, "new_unit": new_unit}

def remove_ingredient(ingredient_data: dict):
    """
    Deletes an ingredient from database.
    
    Args:
        name (str): Ingredient's name.
    
    Returns:
        dict: A message of sucess or fail, with the name of the deleted ingredient.
    
    Example:
        ```python
        remove_ingredient(eggs)
        ```
    """
    session = db_manager.SessionLocal()
    
    if not isinstance(ingredient_data, dict):
        ingredient_data = ingredient_data.model_dump()

    clean_ingredient = normalize_universal_input(ingredient_data)
    name = clean_ingredient["name"]
    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    session.delete(ingredient)
    session.commit()
    session.close()
    return {"status": "success", "deleted": name}
