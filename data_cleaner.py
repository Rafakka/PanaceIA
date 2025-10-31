from schemas import IngredientSchema, RecipeSchema

def normalize_string(value:str) ->str:
    return value.strip().title() if isinstance(value,str) else value

def normalize_quantity(value) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def normalize_unit(value: str) -> str:
    unit_map = {
        "gramas":"Grm",
        "gramos":"Grm",
        "gram":"Grm",
        "gms":"Grm",
        "mls":"Mls",
        "mililitros":"Mls",
        "cps":"Cps",
        "copos":"Cps",
        "copo":"Cp",
        "colher":"Cl",
        "colheres":"Cls",
        "colheres de sopa":"Cls Sopa",
        "colher de sopa":"Cl Sopa",
        "colher de sobremesa":"Cl SobreMs",
        "colheres de sobremesa":"Cls SobreMs",
        "colheres de cha":"Cls Chá",
        "colher de cha":"Cl Chá",
        "xicara":"Xca",
        "xicaras":"Xcas",
        "chicara":"Xca",
        "chicaras":"Xcas",
        "kilos":"Kgs",
        "kilo":"Kg",
        "quilo":"Kg",
        "quilos":"Kgs"
    }

    v= value.strip().lower()
    return unit_map.get(v,v)

def clean_ingredients(data:dict) -> dict:
    return {
        "name":normalize_string(data.get("name")),
        "quantity":normalize_quantity(data.get("quantity")),
        "unit":normalize_unit(data.get("unit"))
    }
    
def clean_recipe(data:dict) -> dict:
    return {
        "name":normalize_string(data.get("name")),
        "steps":normalize_string(data.get("steps")),
        "ingredients":[clean_ingredients(i) for i in data.get("ingredients",[])]
    }

def validate_and_clean_ingredient(raw_data: dict):
    try:
        valid = IngredientSchema(**raw_data)
    except ValidationError as e:
        return {"status": "error", "message": e.errors()}

    clean_data = clean_ingredient(valid.dict())
    return {"status": "success", "data": clean_data}

def validate_and_clean_recipe(raw_data: dict):
    try:
        valid = RecipeSchema(**raw_data)
    except ValidationError as e:
        return {"status": "error", "message": e.errors()}

    clean_data = clean_recipe(valid.dict())
    return {"status": "success", "data": clean_data}