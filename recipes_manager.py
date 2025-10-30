from db_manager import SessionLocal, Recipe, Ingredient, RecipeIngredient

def add_recipe(name, steps, ingredient_data):
    session = SessionLocal()
    recipe = Recipe(name=name, steps=steps)

    for data in ingredient_data:
        ingredient = session.query(ingredient).filter_by(name=data["name"]).first()
        if not ingredient:
            ingredient = Ingredient(name=data["name"], unit=data["unit"])
            session.add(ingredient)
            link = RecipeIngredient (recipe=recipe, ingredient=ingredient, quantity=data["quantity"])
            session.add(link)
            session.commit()
            session.close()

def list_recipes():
    session = SessionLocal()
    recipies = session.query(Recipe.name).all()
    session.close()
    return recipies

