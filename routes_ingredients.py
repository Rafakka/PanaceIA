from fastapi import APIRouter, Body
from ingredients_manager import (
    add_ingredient,
    list_ingredients,
    get_ingredient_name,
    update_ingredient_name,
    update_ingredient_quantity,
    remove_ingredient
)
from data_cleaner import normalize_string, normalize_quantity, apply_cleaning
from schemas import IngredientSchema, UpdateIngredientNameSchema

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.post("/", status_code=201)
def add_ingredient_endpoint(update_data: IngredientSchema):
    cleaning_map = {
        "name":normalize_string,
        "quantity":normalize_quantity,
        "unit":normalize_unit
    }
    clean_update = apply_cleaning(update_data.dict(), cleaning_map)
    return add_ingredient(clean_update)

@router.get("/")
def list_ingredients_endpoint():
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

@router.delete("/", status_code=200)
def delete_ingredient_endpoint(ingredient_data: dict = Body(...)):
    cleaning_map = {
        "name": normalize_string
    }
    clean_data = apply_cleaning(ingredient_data, cleaning_map)
    return remove_ingredient(clean_data)