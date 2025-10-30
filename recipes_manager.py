from db_manager import SessionLocal, Recipe, Ingredient

def add_recipe(name, steps, ingredient_data):
    session = SessionLocal()
    recipe = Recipe(name=name, steps=steps)

    for data in ingredient_data:
        ingredient = session.query(ingredient).filter_by(name=data["name"]).first()
        if not ingredient:
            ingredient = Ingredient(name=data["name"], unit=data["unit"])
            recipe.ingredients.append(ingredient)
        session.add(recipe)
        session.commit()
        session.close()