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
from app.core.data_cleaner import normalize_string, normalize_quantity, normalize_unit, apply_cleaning
from app.core.schemas import RecipeSchema, IngredientSchema

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/")
def list_all_recipes_endpoint():
    return list_recipes()

@router.post("/", status_code=201)
def add_recipe_endpoint(update_data: RecipeSchema):

    cleaning_map = {
        "name": normalize_string,
        "steps": normalize_string
    }
    clean_recipe = apply_cleaning(update_data.dict(), cleaning_map)

    cleaned_ingredients = []
    for ing in update_data.ingredients:
        ing_clean_map = {
            "name": normalize_string,
            "quantity": normalize_quantity,
            "unit": normalize_unit
        }
        cleaned_ingredients.append(apply_cleaning(ing.dict(), ing_clean_map))

    clean_recipe["ingredients"] = cleaned_ingredients
    return add_recipe(clean_recipe)

@router.get("/{name}")
def get_recipe_endpoint(name: str):
    clean_name = normalize_string(name)
    return get_recipe_by_name(clean_name)

@router.delete("/", status_code=200)
def delete_recipe_endpoint(recipe_data: dict = Body(...)):
    cleaning_map = {"name": normalize_string}
    clean_data = apply_cleaning(recipe_data, cleaning_map)
    return remove_recipe(clean_data)

@router.delete("/ingredient", status_code=200)
def delete_ingredient_from_recipe_endpoint(recipe_data: dict = Body(...)):
    cleaning_map = {
        "name": normalize_string,
        "ingredient": normalize_string
    }
    clean_data = apply_cleaning(recipe_data, cleaning_map)
    return remove_ingredient_from_recipe(clean_data)

@router.put("/name", status_code=200)
def update_recipe_name_endpoint(recipe_data: dict = Body(...)):
    cleaning_map = {
        "old_name": normalize_string,
        "new_name": normalize_string
    }
    clean_data = apply_cleaning(recipe_data, cleaning_map)
    return update_recipe_name(clean_data)

@router.put("/ingredient", status_code=200)
def update_recipe_ingredient_endpoint(recipe_data: dict = Body(...)):
    cleaning_map = {
        "recipe_name": normalize_string,
        "old_ingredient": normalize_string,
        "new_ingredient": normalize_string
    }
    clean_data = apply_cleaning(recipe_data, cleaning_map)
    return update_recipe_ingredient(clean_data)

@router.put("/quantity", status_code=200)
def update_recipe_quantity_endpoint(recipe_data: dict = Body(...)):
    cleaning_map = {
        "recipe_name": normalize_string,
        "ingredient": normalize_string,
        "new_quantity": normalize_quantity
    }
    clean_data = apply_cleaning(recipe_data, cleaning_map)
    return update_recipe_quantity(clean_data)
