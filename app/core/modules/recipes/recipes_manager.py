"""
recipes_manager.py

Handles all CRUD operations and logic related to recipes and their ingredients.
Each function here communicates directly with the database through SQLAlchemy ORM
and uses the data_cleaner module for safe input normalization.

All functions return structured dictionaries that can be serialized to JSON
and consumed directly by FastAPI routes.

Author: Rafael Kaher
"""

from app.core import db_manager
from app.core.db_manager import Recipe, Ingredient, RecipeIngredient
from app.core.data_cleaner import normalize_universal_input
from app.core.modules.spices.spices_manager import link_spice_to_recipe
from app.core.modules.spices.spices_manager import auto_learn_from_recipe

def add_recipe(recipe_data: dict):
    """
    Add a new recipe to the database.

    Args:
        recipe_data (dict): A dictionary containing:
            - name (str): Recipe name.
            - steps (str): Preparation instructions.
            - ingredients (list[dict]): Each ingredient dict must include:
                - name (str): Ingredient name.
                - quantity (float): Amount used.
                - unit (str): Unit of measure.

    Returns:
        dict: A status message indicating success or failure.

    Example:
        ```python
        add_recipe({
            "name": "Pancakes",
            "steps": "Mix ingredients and fry until golden.",
            "ingredients": [
                {"name": "Flour", "quantity": 200, "unit": "Grm"}
            ]
        })
        ```
    """
    session = db_manager.SessionLocal()

    clean_recipe = normalize_universal_input(recipe_data)
    if "ingredients" in clean_recipe and isinstance(clean_recipe["ingredients"], list):
        clean_recipe["ingredients"] = [
            normalize_universal_input(ingredient)
            for ingredient in clean_recipe["ingredients"]
            if isinstance(ingredient, dict)
        ]

    name = clean_recipe["name"]
    steps = clean_recipe["steps"]
    ingredient_data = clean_recipe["ingredients"]

    existing = session.query(Recipe).filter_by(name=name).one_or_none()
    if existing:
        session.close()
        return {"status": "error", "message": f"Recipe name '{name}' already exists."}

    recipe = Recipe(name=name, steps=steps)
    session.add(recipe)

    for data in ingredient_data:
        ingredient = session.query(Ingredient).filter_by(name=data["name"]).first()
        if not ingredient:
            ingredient = Ingredient(name=data["name"], unit=data["unit"])
            session.add(ingredient)

        link = RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            quantity=data.get("quantity", 0.0)
        )
        session.add(link)

    session.commit()

    for spice in recipe_data.get("spices", []):
        try:
            from app.core.modules.spices.spices_manager import link_spice_to_recipe
            link_spice_to_recipe(recipe.name, spice)
            auto_learn_from_recipe(recipe.name)
        except Exception as e:
            print(f"⚠️ Warning: could not link spice '{spice}' → {e}")

    session.close()
    return {"status": "success", "message": f"Recipe '{name}' created successfully."}


def list_recipes():

    """
    Retrieve all recipes from the database.

    Returns:
        dict: Contains:
            - status (str): "success" or "error".
            - data (list[dict]): Each recipe includes:
                - name (str)
                - steps (str)

    Example:
        ```python
        list_recipes()
        # -> {"status": "success", "data": [{"name": "Pancakes", "steps": "Mix and fry"}]}
        ```
    """
    
    session = db_manager.SessionLocal()
    recipes = session.query(Recipe).all()
    result = [{"name": r.name, "steps": r.steps} for r in recipes]
    session.close()
    return {"status": "success", "data": result}


def get_recipe_by_name(name: str):

    """
    Retrieve a recipe and its ingredients by name.

    Args:
        name (str): Recipe name.

    Returns:
        dict: Contains:
            - status (str): "success" or "error".
            - data (dict, optional): Includes:
                - name (str)
                - steps (str)
                - ingredients (list[dict]): Each has:
                    - name (str)
                    - quantity (float)
                    - unit (str)

    Example:
        ```python
        get_recipe_by_name("Pancakes")
        ```
    """

    session = db_manager.SessionLocal()

    clean_name = normalize_universal_input(name)
    recipe = session.query(Recipe).filter_by(name=clean_name).one_or_none()
    if not recipe:
        session.close()
        return {"status": "error", "message": f"'{clean_name}' not found."}

    ingredients = [
        {"name": ri.ingredient.name, "quantity": ri.quantity, "unit": ri.ingredient.unit}
        for ri in recipe.recipe_ingredients
    ]
    data = {"name": recipe.name, "steps": recipe.steps, "ingredients": ingredients}
    session.close()
    return {"status": "success", "data": data}


def remove_recipe(recipe_data: dict):
    """
    Delete a recipe from the database.

    Args:
        recipe_data (dict): Must include:
            - name (str): The recipe name to remove.

    Returns:
        dict: A message indicating success or failure.

    Example:
        ```python
        remove_recipe({"name": "Pancakes"})
        ```
    """

    session = db_manager.SessionLocal()
    raw_recipe_name = recipe_data.get("name")
    recipe_name = normalize_universal_input(raw_recipe_name)
    target = session.query(Recipe).filter_by(name=recipe_name).one_or_none()

    if not target:
        session.close()
        return {"status": "error", "message": f"'{recipe_name}' not found."}

    session.delete(target)
    session.commit()
    session.close()
    return {"status": "success", "deleted": recipe_name}


def remove_ingredient_from_recipe(recipe_data: dict):

    """
    Remove a specific ingredient from a recipe.

    Args:
        recipe_data (dict): Must include:
            - name (str): Recipe name.
            - ingredient (str): Ingredient name to remove.

    Returns:
        dict: Updated recipe data or an error message.

    Example:
        ```python
        remove_ingredient_from_recipe({
            "name": "Pancakes",
            "ingredient": "Eggs"
        })
        ```
    """

    session = db_manager.SessionLocal()

    raw_recipe_name = recipe_data.get("name")
    raw_ingredient_name = recipe_data.get("ingredient")

    cleaned_recipe_name = normalize_universal_input(raw_recipe_name)
    ingredient_name = normalize_universal_input(raw_ingredient_name)

    recipe = session.query(Recipe).filter_by(name=cleaned_recipe_name).one_or_none()
    if not recipe:
        session.close()
        return {"status": "error", "message": f"'{cleaned_recipe_name}' not found."}

    for link in recipe.recipe_ingredients:
        if link.ingredient.name == ingredient_name:
            session.delete(link)
            session.commit()
            data = {
                "name": recipe.name,
                "steps": recipe.steps,
                "ingredients": [
                    {"name": ri.ingredient.name, "quantity": ri.quantity, "unit": ri.ingredient.unit}
                    for ri in recipe.recipe_ingredients if ri.ingredient.name != ingredient_name
                ]
            }
            session.close()
            return {"status": "success", "data": data}

    session.close()
    return {"status": "error", "message": f"Ingredient '{ingredient_name}' not found in recipe."}

def update_recipe_name(recipe_data: dict):

    """
    Update a recipe’s name in the database.

    Args:
        recipe_data (dict): Must include:
            - old_name (str): Current recipe name.
            - new_name (str): New name to assign.

    Returns:
        dict: A message indicating whether the update succeeded.

    Example:
        ```python
        update_recipe_name({
            "old_name": "Pancakes",
            "new_name": "Fluffy Pancakes"
        })
        ```
    """

    session = db_manager.SessionLocal()

    clean_recipe = normalize_universal_input(recipe_data)

    old_name = clean_recipe["old_name"]
    new_name = clean_recipe["new_name"]

    target = session.query(Recipe).filter_by(name=old_name).one_or_none()
    if not target:
        session.close()
        return {"status": "error", "message": f"'{old_name}' not found."}
    target.name = new_name
    session.commit()
    session.close()
    return {"status": "success", "updated": old_name, "new_name": new_name}

def update_recipe_ingredient_name(recipe_data: dict):

    """
    Update the name of an ingredient inside a recipe.

    Args:
        recipe_data (dict): Must include:
            - recipe_name (str): Recipe name.
            - old_ingredient (str): Ingredient to rename.
            - new_ingredient (str): New ingredient name.

    Returns:
        dict: Success message or error if ingredient not found.

    Example:
        ```python
        update_recipe_ingredient_name({
            "recipe_name": "Homemade Pasta",
            "old_ingredient": "Brown Flour",
            "new_ingredient": "Flour"
        })
        ```
    """

    session = db_manager.SessionLocal()

    clean_recipe = normalize_universal_input(recipe_data)

    old_ingredient = clean_recipe["old_ingredient"]
    new_ingredient = clean_recipe["new_ingredient"]
    recipe_name = clean_recipe["recipe_name"]

    recipe = session.query(Recipe).filter_by(name=recipe_name).one_or_none()
    if not recipe:
        session.close()
        return {"status": "error", "message": f"'{recipe_name}' not found."}

    for link in recipe.recipe_ingredients:
        if link.ingredient.name == old_ingredient:
            new_ing_obj = session.query(Ingredient).filter_by(name=new_ingredient).one_or_none()
            if not new_ing_obj:
                new_ing_obj = Ingredient(name=new_ingredient, unit=recipe_data.get("unit", ""))
                session.add(new_ing_obj)

            link.ingredient = new_ing_obj
            session.commit()
            session.close()
            return {"status": "success", "updated": old_ingredient, "new_ingredient": new_ingredient}

    session.close()
    return {"status": "error", "message": f"Ingredient '{old_ingredient}' not found in '{recipe_name}'."}

def update_recipe_quantity(recipe_data: dict):

    """
    Update the quantity of a specific ingredient in a recipe.

    Args:
        recipe_data (dict): Must include:
            - recipe_name (str): Target recipe name.
            - ingredient (str): Ingredient to modify.
            - new_quantity (float): Updated quantity value.

    Returns:
        dict: Confirmation message or error message.

    Example:
        ```python
        update_recipe_quantity({
            "recipe_name": "Pancakes",
            "ingredient": "Flour",
            "new_quantity": 250
        })
        ```
    """

    session = db_manager.SessionLocal()

    clean_recipe = normalize_universal_input(recipe_data)

    recipe_name = clean_recipe["recipe_name"]
    ingredient_name = clean_recipe["ingredient"]
    new_quantity = clean_recipe["new_quantity"]

    recipe = session.query(Recipe).filter_by(name=recipe_name).one_or_none()
    if not recipe:
        session.close()
        return {"status": "error", "message": f"'{recipe_name}' not found."}

    for link in recipe.recipe_ingredients:
        if link.ingredient.name == ingredient_name:
            link.quantity = new_quantity
            session.commit()
            session.close()
            return {"status": "success", "updated": ingredient_name, "new_quantity": new_quantity}

    session.close()
    return {"status": "error", "message": f"Ingredient '{ingredient_name}' not found in '{recipe_name}'."}
