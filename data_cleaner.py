def normalize_string(value:str) ->str:
    return value.strip().title() if isinstance(value,str) else value

def normalize_quantity(value) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def normalize_unit(value: str) -> str:
    unit_map = {
        "gramas":"Gm",
        "gramos":"Gm",
        "gram":"Gm",
        "gms":"Gm",
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