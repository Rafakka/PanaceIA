
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_spice_integration_flow():
    """
    Integration test for full recipe → ingredient → spice flow across two databases.
    """

    # 1️⃣ Create a recipe
    recipe = {
        "name": "Banana Cake",
        "steps": "Mash bananas and bake.",
        "ingredients": [
            {"name": "Banana", "quantity": 100, "unit": "Grm"},
            {"name": "Flour", "quantity": 200, "unit": "Grm"},
        ],
    }
    res = client.post("/recipes/", json=recipe)
    assert res.status_code == 201
    assert res.json()["status"] == "success"

    # 2️⃣ Update ingredient quantity
    update_data = {"old_name": "Banana", "new_name": "Banana", "quantity": 150}
    res = client.put("/ingredients/name", json=update_data)
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert res.status_code == 200
    assert "success" in res.json()["status"]
    print(res.json())

    # 3️⃣ Add a spice (goes to its own DB)
    spice = {
        "name": "Cinnamon",
        "flavor_profile": "Warm and sweet",
        "recommended_quantity": "1 tsp per 500g",
        "pairs_with_ingredients": ["Banana", "Flour"],
        "pairs_with_recipes": ["Banana Cake"],
    }
    res = client.post("/spices/", json=spice)
    assert res.status_code == 201
    assert res.json()["status"] == "success"

    # 4️⃣ Link spice → recipe (cross-DB bridge)
    link_data = {"spice_name": "Cinnamon", "recipe_name": "Banana Cake"}
    res = client.post("/spices/link", json=link_data)
    assert res.status_code in (200, 201)
    body = res.json()
    assert body["status"] == "success"
    assert "Cinnamon" in body["message"]
    assert "Banana Cake" in body["message"]
