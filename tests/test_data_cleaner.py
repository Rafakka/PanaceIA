from app.core.data_cleaner import (
    normalize_string,
    normalize_quantity,
    normalize_unit,
    validate_and_clean_ingredient,
    validate_and_clean_recipe
)

def test_normalize_string():
    assert normalize_string("  PANcake  ") == "Pancake"

def test_normalize_quantity():
    assert normalize_quantity("25") == 25.0
    assert normalize_quantity(None) is None

def test_normalize_unit():
    assert normalize_unit("gramas") == "Grm"
    assert normalize_unit("unknownunit") == "unknownunit"

def test_validate_and_clean_ingredient():
    raw = {"name": " milk ", "quantity": "250", "unit": "mls"}
    result = validate_and_clean_ingredient(raw)
    assert result["status"] == "success"
    data = result["data"]
    assert data["name"] == "Milk"
    assert data["quantity"] == 250.0
    assert data["unit"] == "Mls"

def test_validate_and_clean_recipe():
    raw = {
        "name": "pancakes",
        "steps": "mix and fry",
        "ingredients": [
            {"name": "flour", "quantity": "200", "unit": "gramas"},
            {"name": "milk", "quantity": "250", "unit": "mls"}
        ]
    }
    result = validate_and_clean_recipe(raw)
    assert result["status"] == "success"
    assert "data" in result
    assert len(result["data"]["ingredients"]) == 2
