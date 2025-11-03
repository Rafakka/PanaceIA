from fastapi import APIRouter, Body
from recipes_manager import (
    add_recipe,list_recipes,remove_recipe, remove_ingredient_from_recipe,
    update_recipe_name,update_recipe_ingredient,update_recipe_quantity
)
from data_cleaner import normalize_string, normalize_quantity, apply_cleaning
from schemas import RecipeSchema, UpdateIngredientNameSchema

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/")
def list_all_recipes_endpoint():
    return list_recipes()

@router.post("/", status_code=201)
def add_recipe_endpoint(update_data: RecipeSchema):
    cleaning_map = {
        "name":normalize_string,
        "steps":normalize_string,
        "ingredients": List[IngredientSchema]
    }
    clean_update = apply_cleaning(update_data.dict(), cleaning_map)
    return add_ingredient(clean_update)

@router.get("/{name}")
def get_recipe_endpoint(name: str):
    clean_name = normalize_string(name)
    return get_ingredient_name(clean_name)