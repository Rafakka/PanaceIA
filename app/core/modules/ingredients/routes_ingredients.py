"""
routes_ingredients.py

Handles all CRUD operations and logic related to ingredients.
Each function here uses the data_cleaner module for safe input normalization.

Author: Rafael Kaher
"""


from fastapi import APIRouter, Body
from app.core.modules.ingredients.ingredients_manager import (
    add_ingredient,
    list_ingredients,
    get_ingredient_name,
    update_ingredient_name,
    update_ingredient_quantity,
    remove_ingredient
)
from app.core.data_cleaner import normalize_string, normalize_quantity, apply_cleaning, normalize_unit
from app.core.schemas import IngredientSchema, UpdateIngredientNameSchema

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.post("/", status_code=201)
def add_ingredient_endpoint(update_data: IngredientSchema):
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
        add_ingredient_endpoint({
            "name": "Eggs",
            "unit": "Unit.",
            "quantity":"2.0"
        })
        ```
    """
    cleaning_map = {
        "name":normalize_string,
        "quantity":normalize_quantity,
        "unit":normalize_unit
    }
    clean_update = apply_cleaning(update_data.dict(), cleaning_map)
    return add_ingredient(clean_update)

@router.get("/")
def list_ingredients_endpoint():
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
        list_recipes()
        # -> {"status": "success", "data": [{"name": "Flour", "quantity": "100.0", "unit":"Mg"}]}
        ```
    """
    return list_ingredients()

@router.get("/{name}")
def get_ingredient_endpoint(name: str):
    clean_name = normalize_string(name)
    return get_ingredient_name(clean_name)

@router.put("/name", status_code=200)
def update_ingredient_name_endpoint(update_data: UpdateIngredientNameSchema):
    cleaning_map = {
        "old_name": normalize_string,
        "new_name": normalize_string
    }
    clean_update = apply_cleaning(update_data.dict(), cleaning_map)
    return update_ingredient_name(clean_update)

@router.put("/quantity", status_code=200)
def update_ingredient_quantity_endpoint(update_data: dict = Body(...)):
    cleaning_map = {
        "name": normalize_string,
        "new_quantity": normalize_quantity
    }
    clean_update = apply_cleaning(update_data, cleaning_map)
    return update_ingredient_quantity(clean_update)

@router.put("/unit", status_code=200)
def update_ingredient_unit_endpoint(update_data:dict = Body(...)):
    cleaning_map = {
        "name" : normalize_string,
        "new_unit": normalize_string
    }
    clean_update = apply_cleaning(update_data, cleaning_map)
    return update_ingredient_unit(clean_update)

@router.delete("/", status_code=200)
def delete_ingredient_endpoint(ingredient_data: dict = Body(...)):
    cleaning_map = {
        "name": normalize_string
    }
    clean_data = apply_cleaning(ingredient_data, cleaning_map)
    return remove_ingredient(clean_data)