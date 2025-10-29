from db_manager import SessionLocal, Ingredient

def add_ingredient(name, quantity, unit):
    session = SessionLocal()
    ingredients = Ingredient(name=name,quantity=quantity,unit=unit)
    session.add(ingredients)
    session.commit()
    session.close()

def list_ingredients():
    session = SessionLocal()
    ingredients = session.query(Ingredient).all()
    session.close()
    return ingredients

def update_quantity(name, new_quantity):
    session = SessionLocal()
    ingredient = session.query(Ingredient).filter_by(name=name).first()
    if ingredient:
        ingredient.quantity = new_quantity
        session.commit()
    session.close()
    
def remove_ingredient(name):
    session = SessionLocal()
    ingredient = session.query(Ingredient).filter_by(name=name).first()
    if ingredient:
        session.delete(ingredient)
        session.commit()
    session.close()