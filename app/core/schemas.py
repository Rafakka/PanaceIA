"""

schemas.py

Defines the data validation schemas used across the application.

These Pydantic models enforce strict type validation for API inputs and outputs,
ensuring that all data sent to or from the database follows the expected format.

Author: Rafael Kaher

"""

from pydantic import BaseModel, StrictStr, StrictFloat, Field
from typing import List, Optional

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
    flavor_profile: Optional[StrictStr] = None
    recommended_quantity: Optional[StrictStr] = None
    pairs_with_ingredients: List[StrictStr] = Field(default_factory=list)
    pairs_with_recipes: List[StrictStr] = Field(default_factory=list)

class LinkSpiceSchema(BaseModel):
    """
    Schema used for linking spice to recipe.
    Attributes:

        spice_name (str): The spice name to link to a recipe.
        recipe_name (str): The recipe name to be linked.

    Usage Example:
        ```python
        UpdateIngredientNameSchema(
            spice_name="Cinamon",
            recipe_name="Panquekes"
        )
        ```
        
    """
    spice_name: str
    recipe_name: str