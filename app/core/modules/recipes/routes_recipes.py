"""
routes_recipes.py

Handles all recipe CRUD endpoints.
Each endpoint communicates directly with the recipe logic layer
and uses the data_cleaner module to ensure safe input normalization.

All endpoints return structured dictionaries that can be serialized into JSON
and consumed by client applications or automation tools.

Author: Rafael Kaher
"""


from fastapi import APIRouter, Body
from typing import List
from app.core.modules.recipes.recipes_manager import (
    add_recipe,
    list_recipes,
    get_recipe_by_name,
    remove_recipe,
    remove_ingredient_from_recipe,
    update_recipe_name,
    update_recipe_ingredient_name,
    update_recipe_quantity
)
from app.core.decorators import normalize_input
from app.core.schemas import RecipeSchema, IngredientSchema

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/")
def list_all_recipes_endpoint():
    """
    Retrieve all recipes stored in the database.

    Returns:
    A dictionary containing a "status" key and a "data" list with each recipe’s name and steps.

    Example:

    list_all_recipes_endpoint()
    # Returns:
    # {
    #   "status": "success",
    #   "data": [
    #       {"name": "Pancakes", "steps": "Mix and fry"},
    #       {"name": "Omelette", "steps": "Beat and cook"}
    #   ]
    # }
    """
    return list_recipes()

@router.post("/", status_code=201)
@normalize_input
def add_recipe_endpoint(update_data: RecipeSchema):
    """
    Create a new recipe record in the database.
    Input data is automatically cleaned and normalized before storage.

    Args:

        update_data (RecipeSchema): A validated Pydantic object containing:
            name (str): Recipe name.
            steps (str): Preparation instructions.
        ingredients (List[IngredientSchema]): Each ingredient includes:
            name (str)
            quantity (float)
            unit (str)

    Returns:
        A dictionary with a "status" key ("success" or "error") and a message describing the operation result.

    Example:

    add_recipe_endpoint({
        "name": "Pancakes",
        "steps": "Mix ingredients and fry until golden.",
        "ingredients": [
            {"name": "Flour", "quantity": 200, "unit": "Grm"},
            {"name": "Milk", "quantity": 250, "unit": "Mls"}
        ]
    })
    """
    return add_recipe(update_data)

@router.get("/{name}")
@normalize_input
def get_recipe_endpoint(name: str):
    """
    Retrieve a specific recipe and its ingredient details by name.

    Args:
        name (str): The name of the recipe to fetch.

    Returns:
        A dictionary containing the recipe’s name, preparation steps, and a list of ingredients,
        or an error message if the recipe does not exist.

    Example:
        ```python
        get_recipe_endpoint("Pancakes")
        ```
    """
    return get_recipe_by_name(name)

@router.delete("/", status_code=200)
@normalize_input
def delete_recipe_endpoint(recipe_data: dict = Body(...)):
    """
    Delete a recipe record from the database by name.

    Args:
        recipe_data (dict): Must contain:
            name (str): The recipe’s name to delete.

    Returns:
        A dictionary confirming the deletion or indicating that the recipe was not found.

    Example:
        ```python
        delete_recipe_endpoint({"name": "Pancakes"})
        ```
    """
    return remove_recipe(recipe_data)

@router.delete("/ingredient", status_code=200)
@normalize_input
def delete_ingredient_from_recipe_endpoint(recipe_data: dict = Body(...)):
    """
    Remove a specific ingredient from a given recipe.

    Args:
        recipe_data (dict): Must contain:
            name (str): The name of the recipe.
            ingredient (str): The ingredient to remove.

    Returns:
        A dictionary with the updated recipe data excluding the removed ingredient,
        or an error message if the ingredient or recipe could not be found.

    Example:
        ```python
        delete_ingredient_from_recipe_endpoint({
            "name": "Pancakes",
            "ingredient": "Milk"
        })
        ```
    """
    return remove_ingredient_from_recipe(recipe_data)

@router.put("/name", status_code=200)
@normalize_input
def update_recipe_name_endpoint(recipe_data: dict = Body(...)):
    """
    Update the name of an existing recipe.

    Args:
        recipe_data (dict): Must include:
            - `old_name` (str): Current recipe name.
            - `new_name` (str): New name to assign.

    Returns:
        A dictionary confirming the update or an error if the recipe was not found.

    Example:
        ```python
        update_recipe_name_endpoint({
            "old_name": "Pancakes",
            "new_name": "Fluffy Pancakes"
        })
        ```
    """
    return update_recipe_name(recipe_data)

@router.put("/ingredient", status_code=200)
@normalize_input
def update_recipe_ingredient_endpoint(recipe_data: dict = Body(...)):
    """
    Replace one ingredient in a recipe with another.

    Args:
        recipe_data (dict): Must include:
            - `recipe_name` (str): Target recipe.
            - `old_ingredient` (str): Ingredient to replace.
            - `new_ingredient` (str): New ingredient name.

    Returns:
        A status message indicating whether the ingredient was successfully updated or not found.

    Example:
        ```python
        update_recipe_ingredient_endpoint({
            "recipe_name": "Pancakes",
            "old_ingredient": "Milk",
            "new_ingredient": "Oat Milk"
        })
        ```
    """
    return update_recipe_ingredient(recipe_data)

@router.put("/quantity", status_code=200)
@normalize_input
def update_recipe_quantity_endpoint(recipe_data: dict = Body(...)):
    """
    Update the quantity of an ingredient in a recipe.

    Args:
        recipe_data (dict): Must include:
            - `recipe_name` (str): The recipe’s name.
            - `ingredient` (str): Ingredient to modify.
            - `new_quantity` (float): Updated quantity value.

    Returns:
        A dictionary with success or error status and updated quantity details.

    Example:
        ```python
        update_recipe_quantity_endpoint({
            "recipe_name": "Pancakes",
            "ingredient": "Flour",
            "new_quantity": 250
        })
        ```
    """
    return update_recipe_quantity(recipe_data)
