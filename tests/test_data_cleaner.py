
from .app.core.data_cleaner import (
    normalize_string, normalize_quantity, normalize_unit,
    validate_and_clean_ingredient, validate_and_clean_recipe
)
import json


def print_test(title: str, data):
    print(f"\n🔹 {title}")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def test_basic_normalizers():
    print("🚀 Testing basic normalizers...")

    # String normalization
    print_test("normalize_string()", {
        "input": "  panCAKE mix  ",
        "output": normalize_string("  panCAKE mix  ")
    })

    # Quantity normalization
    print_test("normalize_quantity()", {
        "input": "12.5",
        "output": normalize_quantity("12.5")
    })

    # Unit normalization
    print_test("normalize_unit()", {
        "inputs": ["gramas", "kilos", "colher de sopa", "mls", "xicara"],
        "outputs": [normalize_unit(u) for u in ["gramas", "kilos", "colher de sopa", "mls", "xicara"]]
    })


def test_ingredient_validation():
    print("\n🧩 Testing ingredient validation...")

    messy_ingredient = {
        "name": "  flour  ",
        "quantity": "  200 ",
        "unit": "gramas"
    }

    result = validate_and_clean_ingredient(messy_ingredient)
    print_test("validate_and_clean_ingredient()", result)


def test_recipe_validation():
    print("\n🍳 Testing recipe validation...")

    messy_recipe = {
        "name": "  PANCAKES  ",
        "steps": "  mix ingredients and fry until golden ",
        "ingredients": [
            {"name": "  flour ", "quantity": "200", "unit": "gramas"},
            {"name": "  Milk", "quantity": " 250 ", "unit": "mls"},
            {"name": " eGG ", "quantity": "2", "unit": "pcs"}
        ]
    }

    result = validate_and_clean_recipe(messy_recipe)
    print_test("validate_and_clean_recipe()", result)


if __name__ == "__main__":
    print("🧠 Starting Data Cleaner Tests...")
    test_basic_normalizers()
    test_ingredient_validation()
    test_recipe_validation()
    print("\n✅ All cleaner tests executed.\n")
