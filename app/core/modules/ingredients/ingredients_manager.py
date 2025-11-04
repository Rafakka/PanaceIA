"""
ingredients_manager.py

Handles all CRUD operations and logic related to ingredients only.
Each function here communicates directly with the database through SQLAlchemy ORM
and uses the data_cleaner module for safe input normalization.

All functions return structured dictionaries that can be serialized to JSON
and consumed directly by FastAPI routes.

Author: Rafael Kaher
"""


from app.core.db_manager import SessionLocal, Ingredient
from app.core.data_cleaner import normalize_string, normalize_quantity, normalize_unit

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
    session = SessionLocal()

    ingredient_clean_map = {
        "name": normalize_string,
        "quantity": normalize_quantity,
        "unit":normalize_unit
    }

    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)

    name = clean_ingredient["name"]
    quantity = clean_ingredient["quantity"]
    unit = clean_ingredient["unit"]


    ingredient = session.query(Ingredient).filter_by(name=data["name"]).first()
    if not ingredient:
        ingredient = Ingredient(name=name, unit=unit)
        session.add(ingredient)

        link = RecipeIngredient(
        recipe=recipe,
        ingredient=ingredient,
        quantity=data["quantity"]
        )
        session.commit(link)
        session.close()
        return {"status": "success", "name": name}

    session.close()
    return {"status": "error","message": f" Ingredient, '{name}' already in Database."}

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
    session = SessionLocal()
    ingredients = session.query(Ingredient).all()
    result = [
        {"name": i.name, "quantity": i.quantity, "unit": i.unit}
        for i in ingredients
    ]
    session.close()
    return result

def get_ingredient_name(name: str):
    """
    Retrieve a ingredient by name.

    Args:
        name (str): Ingredient's name.

    Returns:
        dict: Contains:
            - status (str): "success" or "error".
            - ingredient (list[dict]):
                - name (str)
                - quantity (float)
                - unit (str)

    Example:
        ```python
        get_ingredient_name("eggs")
        ```
    """
    session = SessionLocal()
    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}
    data = {
        "name": ingredient.name,
        "quantity": ingredient.quantity,
        "unit": ingredient.unit
    }
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
    session = SessionLocal()

    ingredient_clean_map = {
        "old_name": normalize_string,
        "new_name": normalize_string
    }

    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)

    old_name = clean_ingredient["old_name"]
    new_name = clean_ingredient["new_name"]

    ingredient = session.query(Ingredient).filter_by(name=old_name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{old_name}' not found."}
    ingredient.name = new_name
    session.commit()
    data = {
        "name": ingredient.name,
        "quantity": ingredient.quantity,
        "unit": ingredient.unit
    }
    session.close()
    return {"status": "success", "updated": old_name, "new_name": new_name}


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

    session = SessionLocal()

    ingredient_clean_map = {
        "name": normalize_string,
        "new_quantity": normalize_quantity
    }

    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)

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
    session = SessionLocal()

    ingredient_clean_map = {
        "name": normalize_string,
        "new_unit": normalize_unit
    }

    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)

    name = clean_ingredient["name"]
    new_unit = clean_ingredient["new_unit"]

    name = ingredient_data.get("name")
    new_quantity = ingredient_data.get("new_unit")

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
    session = SessionLocal()
    ingredient_clean_map = {
        "name": normalize_string
    }
    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)
    name = clean_ingredient["name"]
    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    session.delete(ingredient)
    session.commit()
    session.close()
    return {"status": "success", "deleted": name}
