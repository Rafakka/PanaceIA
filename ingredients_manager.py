from db_manager import SessionLocal, Ingredient
from data_cleaner import normalize_string, normalize_quantity, normalize_unit

def add_ingredient(ingredient_data: dict):
    session = SessionLocal()

    ingredient_clean_map = {
        "name": normalize_string,
        "quantity": normalize_quantity,
        "unit":normalize_unit
    }

    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)

    name = clean_ingredient["name"]
    quantity = clean_ingredient["quantity"]
    unit = clean_ingredient["unit"]


    ingredient = session.query(Ingredient).filter_by(name=data["name"]).first()
    if not ingredient:
        ingredient = Ingredient(name=name, unit=unit)
        session.add(ingredient)

        link = RecipeIngredient(
        recipe=recipe,
        ingredient=ingredient,
        quantity=data["quantity"]
        )
        session.commit(link)
        session.close()
        return {"status": "success", "name": name}

    session.close()
    return {"status": "error","message": f" Ingredient, '{name}' already in Database."}

def list_ingredients():
    session = SessionLocal()
    ingredients = session.query(Ingredient).all()
    result = [
        {"name": i.name, "quantity": i.quantity, "unit": i.unit}
        for i in ingredients
    ]
    session.close()
    return result

def get_ingredient_name(name: str):
    session = SessionLocal()
    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}
    data = {
        "name": ingredient.name,
        "quantity": ingredient.quantity,
        "unit": ingredient.unit
    }
    session.close()
    return {"status": "success", "data": data}

def update_ingredient_name(ingredient_data: dict):
    session = SessionLocal()

    ingredient_clean_map = {
        "old_name": normalize_string,
        "new_name": normalize_string
    }

    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)

    old_name = clean_ingredient["old_name"]
    new_name = clean_ingredient["new_name"]

    ingredient = session.query(Ingredient).filter_by(name=old_name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{old_name}' not found."}
    ingredient.name = new_name
    session.commit()
    data = {
        "name": ingredient.name,
        "quantity": ingredient.quantity,
        "unit": ingredient.unit
    }
    session.close()
    return {"status": "success", "updated": old_name, "new_name": new_name}


def update_ingredient_quantity(ingredient_data: dict):
    session = SessionLocal()

    ingredient_clean_map = {
        "name": normalize_string,
        "new_quantity": normalize_quantity
    }

    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)

    name = clean_ingredient["name"]
    new_quantity = clean_ingredient["new_quantity"]

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}
    ingredient.quantity = new_quantity
    session.commit()
    session.close()
    return {"status": "success", "ingredient": name, "new_quantity": new_quantity}

def update_ingredient_unit(ingredient_data: dict):
    session = SessionLocal()

    ingredient_clean_map = {
        "name": normalize_string,
        "new_unit": normalize_unit
    }

    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)

    name = clean_ingredient["name"]
    new_unit = clean_ingredient["new_unit"]

    name = ingredient_data.get("name")
    new_quantity = ingredient_data.get("new_unit")

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    ingredient.unit = new_unit
    session.commit()
    session.close()
    return {"status": "success", "ingredient": name, "new_unit": new_unit}

def remove_ingredient(ingredient_data: dict):
    session = SessionLocal()
    ingredient_clean_map = {
        "name": normalize_string
    }
    clean_ingredient = apply_cleaning(ingredient_data, ingredient_clean_map)
    name = clean_ingredient["name"]
    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    session.delete(ingredient)
    session.commit()
    session.close()
    return {"status": "success", "deleted": name}
