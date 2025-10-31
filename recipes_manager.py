from db_manager import SessionLocal, Recipe, Ingredient, RecipeIngredient

def add_recipe(recipe_data:dict):
    name  = recipe_data["name"]
    steps = recipe_data["steps"]
    ingredient_data = recipe_data["ingredients"]

    session = SessionLocal()
    recipe = Recipe(name=name, steps=steps)
    session.add(recipe)

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

def remove_recipe(recipe_data:dict):
    session = SessionLocal()
    recipe_name  = recipe_data.get("name")

    target = session.query(Recipe).filter_by(name=recipe_name).one_or_none()
    
    if target:
        session.delete(target)
        session.commit()
    session.close()

def remove_ingredient_from_recipe(recipe_data:dict):
    session = SessionLocal()

    recipe_name = recipe_data.get("name")
    ingredient_name = recipe_data.get("ingredient")

    target = session.query(Recipe).filter_by(name=recipe_name).one_or_none()
    if not target:
        session.close()
        return
    for link in target.recipe_ingredients:
        if link.ingredient.name == ingredient_name:
            session.delete(link)
            session.commit()
            session.close()
            return     
    session.close()

def update_recipe_name(recipe_data:dict):
    session = SessionLocal()

    old_name = recipe_data.get("old_name")
    new_name = recipe_data.get("new_name")

    target = session.query(Recipe).filter_by(name=old_name).one_or_none()
    if not target:
        session.close()
        return
    if target:
        target.name = new_name
        session.commit()
    session.close()

def update_recipe_ingredient(recipe_data:dict):
    session = SessionLocal()
    
    recipe_name = recipe_data.get("recipe_name")
    old_ingredient = recipe_data.get("old_ingredient")
    new_ingredient = recipe_data.get("new_ingredient")
    
    target = session.query(Recipe).filter_by(name=recipe_name).one_or_none()
    if not target:
        session.close()
        return
    for link in target.recipe_ingredients:
        if link.ingredient.name == old_ingredient:
            new_ing_obj = session.query(Ingredient).filter_by(name=new_ingredient).one_or_none()
            if not new_ing_obj:
                new_ing_obj = Ingredient(name=new_ingredient)
                session.add(new_ing_obj)
            link.ingredient = new_ing_obj
            session.commit()
            session.close()
            return
    session.close()

def update_recipe_quantity(recipe_data:dict):
    session = SessionLocal()

    recipe_name = recipe_data("recipe_name")
    ingredient = recipe_data("ingredient")
    new_quantity = recipe_data("new_quantity")

    target = session.query(Recipe).filter_by(name=recipe_name).one_or_none()
    if not target:
        session.close()
        return
    for link in target.recipe_ingredients:
        if link.ingredient.name == ingredient:
            link.quantity = new_quantity
            session.commit()
            session.close()
            return     
        session.commit()
    session.close()