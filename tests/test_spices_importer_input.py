import json
import pytest
from app.core.modules.import_gateway.import_manager import import_single_recipe, import_bulk_recipes
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recipe_input_importer_valid():
    """
    When valid data is given, the importer should:
    - Normalize names and units
    - Return 'success' status
    - Include cleaned data under 'data'
    """
    raw_data = {
        "name": "panCakes",
        "steps": "miX and fRy",
        "ingredients": [
            {"name": "flOUr", "quantity": "210", "unit": "gramas"},
            {"name": "miLk", "quantity": "225", "unit": "mililitros"},
        ],
    }

    expected = {"status": "success", "data": {...}}

    result = import_single_recipe(raw_data)

    assert result["status"] == "success", f"Recipe {i} should have succeeded."
    assert "data" in result


def test_recipe_input_importer_invalid():
    """
    When required fields are missing or malformed,
    the importer should:
    - Return 'error' status
    - Include a meaningful error message
    """
    raw = {
        # Missing "steps"
        "name": "Omelette",
        "ingredients": [
            {"name": "Egg", "quantity": "", "unit": "unit"},
        ],
    }

    result = import_single_recipe(raw)

    assert result["status"] == "error"
    assert "invalid" in result["message"].lower()

def test_recipe_input_importer_bulk_mixed_valid_invalid():

    """
    Test bulk import of multiple recipes:
    - Each recipe should be normalized correctly
    - All results must have 'success' status
    - The number of outputs should match the inputs
    """

    recipe1 = {
        "name": "panCakes",
        "steps": "miX and fRy",
        "ingredients": [
            {"name": "flOUr", "quantity": "210", "unit": "gramas"},
            {"name": "miLk", "quantity": "225", "unit": "mililitros"}
        ]
    }
    recipe2 = {
        "name": "spagaTTi with sAUce",
        "steps": "boil, let it DRY, pour toMAto sauce OVER it.",
        "ingredients": [
            {"name": "spaGGeti", "quantity": "", "unit": "gramos"},
            {"name": "TomATO SAuce", "quantity": "250", "unit": "copos"}
        ]
    }
    recipe3 = {
        "name": "BaSIS cAKe",
        "steps": "Mix dry ingredients, mix liquid, bake it in the ovEN, 30 mIN to 40 MIn",
        "ingredients": [
            {"name": "flOUr", "quantity": "400", "unit": "gramas"},
            {"name": "mILk", "quantity": "300", "unit": "militros"},
            {"name": "eGGS", "quantity": "3", "unit": " "}
        ]
    }
    recipe4 = {
        "name": "cooKies",
        "steps": "Mix dry ingredients, mix liquid, bake it in the ovEN, 10 mIN to 20 MIn",
        "ingredients": [
            {"name": "flOUr", "quantity": "400", "unit": "gramas"},
            {"name": "Butter", "quantity": "250.0", "unit": "gramos"},
            {"name": "eGGS", "quantity": "2", "unit": " "}
        ]
    }


    input_data = [recipe1, recipe2, recipe3, recipe4]

    expected_results = [
    {"status": "success", "data": {...}}, 
    {"status": "error", "message": "Invalid quantity"},
    {"status": "success", "data": {...}},
    {"status": "success", "data": {...}}
    ]

    result = import_bulk_recipes(input_data)

    for i, (expected, actual) in enumerate(zip(expected_results, result), start=1):
        if expected["status"] == "success":
            assert actual["status"] == "success", f"Recipe {i} should have succeeded."
            assert "data" in actual
        else:
            assert actual["status"] == "error", f"Recipe {i} should have failed."
            assert "message" in actual