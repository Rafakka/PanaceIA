from fastapi import APIRouter, Body
from ingredients_manager import (
    add_ingredient,
    list_ingredients,
    get_ingredient_name,
    update_ingredient_name,
    update_ingredient_quantity,
    remove_ingredient
)
from data_cleaner import normalize_string, normalize_quantity, clean_ingredient
from schemas import IngredientSchema, UpdateIngredientNameSchema

router = APIRouter(prefix="/ingredients", tags=["ingredients"])

@router.post("/", status_code=201)
def add_ingredient_endpoint(ingredient: IngredientSchema):
    clean_data = clean_ingredient(ingredient.dict())
    result = add_ingredient(clean_data)
    return result

@router.get("/")
def list_ingredients_endpoint():
    return list_ingredients()

@router.get("/{name}")
def get_ingredient_endpoint(name: str):
    clean_name = normalize_string(name)
    return get_ingredient_name(clean_name)

@router.put("/name", status_code=200)
def update_ingredient_name_endpoint(update_data: UpdateIngredientNameSchema):
    old_name = normalize_string(update_data.old_name)
    new_name = normalize_string(update_data.new_name)
    return update_ingredient_name({"old_name": old_name, "new_name": new_name})

@router.put("/quantity", status_code=200)
def update_ingredient_quantity_endpoint(update_data: dict = Body(...)):
    name = normalize_string(update_data.get("name"))
    raw_quantity = update_data.get("new_quantity")
    new_quantity = normalize_quantity(raw_quantity)
    return update_ingredient_quantity({"name": name, "new_quantity": new_quantity})

@router.delete("/", status_code=200)
def delete_ingredient_endpoint(ingredient_data: dict = Body(...)):
    name = normalize_string(ingredient_data.get("name"))
    return remove_ingredient({"name": name})