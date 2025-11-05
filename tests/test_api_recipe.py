import json

def test_recipe_crud_flow(test_client):
    recipe = {
        "name": "Pancakes",
        "steps": "Mix and fry",
        "ingredients": [
            {"name": "Flour", "quantity": 200, "unit": "Grm"},
            {"name": "Milk", "quantity": 250, "unit": "Mls"}
        ]
    }

    # Create
    res = test_client.post("/recipes/", json=recipe)
    assert res.status_code == 201
    assert res.json()["status"] == "success"

    # List
    res = test_client.get("/recipes/")
    assert res.status_code == 200
    assert any(r["name"] == "Pancakes" for r in res.json()["data"])

    # Get by name
    res = test_client.get("/recipes/Pancakes")
    assert res.status_code == 200
    assert res.json()["data"]["name"] == "Pancakes"

    # Update name
    res = test_client.put("/recipes/name", json={"old_name": "Pancakes", "new_name": "Fluffy Pancakes"})
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # Delete
    res = test_client.request("DELETE", "/recipes/", json={"name": "Fluffy Pancakes"})
    assert res.status_code == 200
    assert res.json()["status"] == "success"
