import json

def test_import_single_recipe(test_client):
    recipe = {
        "name": "Pancakes",
        "steps": "Mix and fry",
        "ingredients": [
            {"name": "Flour", "quantity": 200, "unit": "Grm"},
            {"name": "Milk", "quantity": 250, "unit": "Mls"}
        ]
    }
    res = test_client.post("/import/recipe", json=recipe)
    assert res.status_code == 201
    assert res.json()["status"] == "success"

def test_import_bulk_recipe(test_client):

    recipes = [{
        "name": "Pancakes",
        "steps": "Mix and fry",
        "ingredients": [
            {"name": "Flour", "quantity": 200, "unit": "Grm"},
            {"name": "Milk", "quantity": 250, "unit": "Mls"}
        ]
    },{
        "name": "Cake Base",
        "steps": "Mix liquid, mix dry ingredients, mix them together and put on the oven",
        "ingredients": [
            {"name": "Flour", "quantity": 200, "unit": "Grm"},
            {"name": "Milk", "quantity": 250, "unit": "Mls"}
        ]
    }, {
        "name": "Rice",
        "steps": "Mix in pan with olive oil, fry stir then pour water",
        "ingredients": [
            {"name": "Rice", "quantity": 200, "unit": "Grm"},
            {"name": "Olive oil", "quantity": 250, "unit": "Mls"}
        ]
    }
    ]
    res = test_client.post("/import/bulk", json=recipes)
    assert res.status_code == 201
    for item in res.json():
        assert item["status"] == "success"
