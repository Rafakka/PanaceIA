from db_manager import SessionLocal, Ingredient

def add_ingredient(ingredient_data:dict):

    session = SessionLocal()
    name = ingredient_data.get("name") 
    quantity = ingredient_data.get("quantity") 
    unit = ingredient_data.get("unit")

    ingredients = Ingredient(name=name,quantity=quantity,unit=unit)
    session.add(ingredients)
    session.commit()
    session.close()

def list_ingredients():
    session = SessionLocal()
    ingredients = session.query(Ingredient).all()
    session.close()
    return ingredients

def update_ingredient_name(ingredient_data:dict):
    session = SessionLocal()

    old_name = ingredient_data.get("old_name") 
    new_name = ingredient_data.get("new_name")

    ingredient = session.query(Ingredient).filter_by(name=old_name).one_or_none()
    if ingredient:
        ingredient.name = new_name
        session.commit()
    session.close()

def update_ingredient_quantity(ingredient_data:dict):
    session = SessionLocal()

    name = ingredient_data.get("name") 
    new_quantity = ingredient_data.get("new_quantity")

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if ingredient:
        ingredient.quantity = new_quantity
        session.commit()
    session.close()

def remove_ingredient(ingredient_data:dict):
    session = SessionLocal()

    name = ingredient_data.get("name")

    ingredient = session.query(Ingredient).filter_by(name=name).one_or_none()
    if ingredient:
        session.delete(ingredient)
        session.commit()
    session.close()