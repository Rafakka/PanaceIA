from app.core.data_cleaner import normalize_universal_input
import pytest

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

def test_normalize_universal_input_with_simple_string():
    result = normalize_universal_input("  milk ")
    assert result == "Milk"

def test_normalize_universal_input_with_number_string():
    result = normalize_universal_input(" 200 ")
    assert result == 200.0

def test_normalize_universal_input_with_unknown_type():
    result = normalize_universal_input(None)
    assert result is None

def test_normalize_universal_input_with_basic_dict():
    raw = {"name": "  sugar  ", "quantity": " 200 ", "unit": "gramas"}
    result = normalize_universal_input(raw)
    assert result == {"name": "Sugar", "quantity": 200.0, "unit": "Grm"}

def test_normalize_universal_input_with_semantic_keys():
    raw = {
        "new_name": " flour ",
        "old_quantity": " 150 ",
        "base_unit": "mls"
    }
    result = normalize_universal_input(raw)
    assert result == {
        "new_name": "Flour",
        "old_quantity": 150.0,
        "base_unit": "Mls"
    }

def test_normalize_universal_input_ignores_unapproved_fields():
    raw = {"username": "  chef01 ", "email": " user@example.com "}
    result = normalize_universal_input(raw)
    # should remain untouched
    assert result == raw

def test_normalize_universal_input_mixed_fields():
    raw = {
        "name": "  butter ",
        "temperature": "cold",
        "unit": "copo"
    }
    result = normalize_universal_input(raw)
    assert result == {
        "name": "Butter",
        "temperature": "cold",  # unchanged
        "unit": "Cp"
    }

def test_normalize_universal_input_with_nested_dict():
    raw = {
        "ingredient": {"name": "  oil  ", "unit": "mls"},
        "metadata": {"creator": "chef"}
    }
    result = normalize_universal_input(raw)
    # inner dict stays untouched because you don’t recursively clean (yet)
    assert result == raw

def test_normalize_universal_input_fault_tolerance(monkeypatch):
    def bad_cleaner(value):
        raise ValueError("oops")

    # temporarily add a broken cleaner
    import app.core.data_cleaner as cleaner_module
    cleaner_module.normalize_bad = bad_cleaner

    raw = {"bad": "test"}
    result = normalize_universal_input(raw)

    assert result == {"bad": "test"}

def test_full_scenario_cleaning():
    messy_input = {
        "new_name": "  banana  ",
        "quantity": " 50 ",
        "unit": "gramas",
        "username": " admin "
    }

    expected = {
        "new_name": "Banana",
        "quantity": 50.0,
        "unit": "Grm",
        "username": " admin "
    }

    result = normalize_universal_input(messy_input)
    assert result == expected