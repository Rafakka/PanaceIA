from db_manager import SessionLocal, Recipe, Ingredient, RecipeIngredient
from data_cleaner import normalize_string, normalize_quantity, normalize_unit, apply_cleaning

def add_recipe(recipe_data: dict):
    session = SessionLocal()

    recipe_clean_map = {
        "name": normalize_string,
        "steps": normalize_string
    }
    clean_recipe = apply_cleaning(recipe_data, recipe_clean_map)

    name = clean_recipe["name"]
    steps = clean_recipe["steps"]
    ingredient_data = recipe_data["ingredients"]

    cleaned_ingredients = [
        apply_cleaning(ing, {
            "name": normalize_string,
            "quantity": normalize_quantity,
            "unit": normalize_unit
        }) for ing in ingredient_data
    ]

    existing_recipe = session.query(Recipe).filter_by(name=name).first()
    if existing_recipe:
        session.close()
        return {"status": "error", "message": f"Recipe '{name}' already in DB."}

    recipe = Recipe(name=name, steps=steps)
    session.add(recipe)

    for data in cleaned_ingredients:
            ingredient = session.query(Ingredient).filter_by(name=data["name"]).first()
            if not ingredient:
                ingredient = Ingredient(name=data["name"], unit=data["unit"])
                session.add(ingredient)

            link = RecipeIngredient(recipe=recipe, ingredient=ingredient, quantity=data["quantity"])
            session.add(link)

    session.commit()
    session.close()
    return {"status": "success", "message": f"Recipe '{name}' created successfully."}


def list_recipes():
    session = SessionLocal()
    recipes = session.query(Recipe).all()
    result = [
        {"name": r.name, "steps": r.steps}
        for r in recipes
    ]
    session.close()
    return {"status": "success", "data": result}

def get_recipe_by_name(name: str):
    session = SessionLocal()
    recipe = session.query(Recipe).filter_by(name=name).one_or_none()

    if not recipe:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    ingredients = [
        {
            "name": ri.ingredient.name,
            "quantity": ri.quantity,
            "unit": ri.ingredient.unit
        }
        for ri in recipe.recipe_ingredients
    ]

    data = {
        "name": recipe.name,
        "steps": recipe.steps,
        "ingredients": ingredients
    }

    session.close()
    return {"status": "success", "data": data}

def remove_recipe(recipe_data: dict):
    session = SessionLocal()
    recipe_name = recipe_data.get("name")
    target = session.query(Recipe).filter_by(name=recipe_name).one_or_none()

    if not target:
        session.close()
        return {"status": "error", "message": f"'{recipe_name}' not found."}

    session.delete(target)
    session.commit()
    session.close()
    return {"status": "success", "deleted": recipe_name}

def remove_ingredient_from_recipe(recipe_data: dict):
    session = SessionLocal()
    recipe_name = recipe_data.get("name")
    ingredient_name = recipe_data.get("ingredient")

    recipe = session.query(Recipe).filter_by(name=recipe_name).one_or_none()
    if not recipe:
        session.close()
        return {"status": "error", "message": f"'{recipe_name}' not found."}

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

def update_recipe_name(recipe_data:dict):
    session = SessionLocal()

    old_name = recipe_data.get("old_name")
    new_name = recipe_data.get("new_name")

    target = session.query(Recipe).filter_by(name=old_name).one_or_none()
    if not target:
        session.close()
        return {"status": "error", "message": f"'{old_name}' not found."}
    if target:
        target.name = new_name
        session.commit()
        session.close()
        return {"status": "success", "updated": old_name, "new_name": new_name}

def update_recipe_ingredient(recipe_data: dict):
    session = SessionLocal()
    recipe_name = recipe_data.get("recipe_name")
    old_ingredient = recipe_data.get("old_ingredient")
    new_ingredient = recipe_data.get("new_ingredient")

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
    session = SessionLocal()
    recipe_name = recipe_data.get("recipe_name")
    ingredient_name = recipe_data.get("ingredient")
    new_quantity = recipe_data.get("new_quantity")

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

