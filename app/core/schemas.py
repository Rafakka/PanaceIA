from pydantic import BaseModel, StrictStr, StrictFloat
from typing import List

class IngredientSchema(BaseModel):
    name: StrictStr
    quantity: StrictFloat
    unit: StrictStr

class RecipeSchema(BaseModel):
    name: StrictStr
    steps: StrictStr
    ingredients: List[IngredientSchema]

class UpdateIngredientNameSchema(BaseModel):
    old_name: str
    new_name: str