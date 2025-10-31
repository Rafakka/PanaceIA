from db_manager import SessionLocal, Ingredient

def add_ingredient(ingredient_data: dict):
    session = SessionLocal()
    name = ingredient_data.get("name")
    quantity = ingredient_data.get("quantity")
    unit = ingredient_data.get("unit")

    if not name:
        session.close()
        return {"status": "error", "message": "Ingredient name is required."}

    ingredient = Ingredient(name=name, quantity=quantity, unit=unit)
    session.add(ingredient)
    session.commit()
    session.close()
    return {"status": "success", "name": name}


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
    old_name = ingredient_data.get("old_name")
    new_name = ingredient_data.get("new_name")

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
    name = ingredient_data.get("name")
    new_quantity = ingredient_data.get("new_quantity")

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    ingredient.quantity = new_quantity
    session.commit()
    session.close()
    return {"status": "success", "ingredient": name, "new_quantity": new_quantity}


def remove_ingredient(ingredient_data: dict):
    session = SessionLocal()
    name = ingredient_data.get("name")

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if not ingredient:
        session.close()
        return {"status": "error", "message": f"'{name}' not found."}

    session.delete(ingredient)
    session.commit()
    session.close()
    return {"status": "success", "deleted": name}
