"""

schemas.py

Defines the data validation schemas used across the application.

These Pydantic models enforce strict type validation for API inputs and outputs,
ensuring that all data sent to or from the database follows the expected format.

Author: Rafael Kaher

"""

from pydantic import BaseModel, StrictStr, StrictFloat
from typing import List

class IngredientSchema(BaseModel):
    """

    Represents the schema for an ingredient object used in recipes.

    Attributes:
        name (StrictStr): Ingredient name.
        quantity (StrictFloat): Ingredient amount (must be a float).
        unit (StrictStr): Measurement unit (e.g., "Grm", "Mls", "Cp").

    Example:
        ```python
        IngredientSchema(
        name="Flour",
        quantity=200.0,
        unit="Grm"
        )
        ```
    """
    name: StrictStr
    quantity: StrictFloat
    unit: StrictStr

class RecipeSchema(BaseModel):
    """

    Defines the schema for a complete recipe,
    including its basic information and a list of ingredients.

    Attributes:
        name (StrictStr): Recipe name.
        steps (StrictStr): Preparation instructions.
        ingredients (List[IngredientSchema]): List of ingredients following the IngredientSchema model.

    Usage Example:
        ```python
        RecipeSchema(
            name="Pancakes",
            steps="Mix ingredients and fry until golden.",
            ingredients=[
                IngredientSchema(name="Flour", quantity=200.0, unit="Grm"),
                IngredientSchema(name="Milk", quantity=250.0, unit="Mls")
            ]
        )
        ```
    """

    name: StrictStr
    steps: StrictStr
    ingredients: List[IngredientSchema]
    spices: List[StrictStr] = []

class UpdateIngredientNameSchema(BaseModel):
    """
    Schema used for updating an ingredient’s name in the system.

    Attributes:

        old_name (str): The current ingredient name.
        new_name (str): The desired new name.

    Usage Example:
        ```python
        UpdateIngredientNameSchema(
            old_name="Milk",
            new_name="Oat Milk"
        )
        ```
        
    """
    old_name: str
    new_name: str

class SpiceSchema(BaseModel):
    """
    Represents a spice object with all contextual attributes used for learning and suggestions.
    
    Attributes:
        name (str): Spice name.
        flavor_profile (str): Description of its taste (e.g., "warm and sweet").
        recommended_quantity (str): Suggested usage, e.g., "1 tsp per 500g".
        pairs_with_ingredients (List[str]): Ingredients it matches with.
        pairs_with_recipes (List[str]): Recipes it commonly appears in.
    """

    name: StrictStr
    flavor_profile: StrictStr | None = None
    recommended_quantity: StrictStr | None = None
    pairs_with_ingredients: List[StrictStr] = []
    pairs_with_recipes: List[StrictStr] = []