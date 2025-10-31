from fastapi import APIRouter, Body
from ingredients_manager import (
    add_ingredient,
    list_ingredients,
    get_ingredient_name,
    update_ingredient_name,
    update_ingredient_quantity,
    remove_ingredient
)
from data_cleaner import normalize_string, clean_ingredient
from schemas import IngredientSchema, UpdateIngredientNameSchema

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.post("/", status_code=201)
def add_ingredient_endpoint(ingredient: IngredientSchema):
    clean_data = clean_ingredient(ingredient.dict())
    result = add_ingredient(clean_data)
    return result

@router.get("/")
def list_ingredients_endpoint():
    result = list_ingredients()
    return result

@router.get("/{name}")
def get_ingredient_endpoint(name: str):
    clean_name = normalize_string(name)
    result = get_ingredient_name(clean_name)
    return result

@router.put("/name")
def update_ingredient_name_endpoint(update_data: UpdateIngredientNameSchema):
    old_name = normalize_string(update_data.old_name)
    new_name = normalize_string(update_data.new_name)
    result = update_ingredient_name({"old_name": old_name, "new_name": new_name})
    return result

@router.put("/quantity")
def update_ingredient_quantity_endpoint(update_data: dict = Body(...)):
    name = normalize_string(update_data.get("name"))
    new_quantity = update_data.get("new_quantity")
    result = update_ingredient_quantity({"name": name, "new_quantity": new_quantity})
    return result

@router.delete("/")
def delete_ingredient_endpoint(ingredient_data: dict = Body(...)):
    name = normalize_string(ingredient_data.get("name"))
    result = remove_ingredient({"name": name})
    return result
