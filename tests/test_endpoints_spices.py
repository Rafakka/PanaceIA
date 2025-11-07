import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.usefixtures("setup_test_dbs")
def test_add_and_list_spices():
    """Test creating and listing spices."""
    spice = {
        "name": "Cinnamon",
        "flavor_profile": "Warm and sweet",
        "recommended_quantity": "1 tsp per 500g",
        "pairs_with_ingredients": ["Apple", "Sugar"],
        "pairs_with_recipes": ["Apple Pie"],
    }

    # Add spice
    res = client.post("/spices/", json=spice)
    assert res.status_code == 201
    data = res.json()
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert data["status"] == "success"
    assert "Cinnamon" in data["message"]

    # List all spices
    res = client.get("/spices/")
    assert res.status_code == 200
    data = res.json()
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert isinstance(data, list)
    assert any(sp["name"] == "Cinnamon" for sp in data)


@pytest.mark.usefixtures("setup_test_dbs")
def test_update_spice():
    """Test updating spice attributes."""
    # Create spice first
    spice = {
        "name": "Nutmeg",
        "flavor_profile": "Warm and spicy",
        "recommended_quantity": "½ tsp per 500g",
        "pairs_with_ingredients": [],
        "pairs_with_recipes": [],
    }
    res = client.post("/spices/", json=spice)
    assert res.status_code == 201

    # Update spice
    update_data = {
        "name": "Nutmeg",
        "flavor_profile": "Sweet and aromatic",
        "recommended_quantity": "¼ tsp per 500g",
    }
    res = client.put("/spices/", json=update_data)
    assert res.status_code == 200
    data = res.json()
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert data["status"] == "success"
    assert "Nutmeg" in data["message"]

    # Verify update
    res = client.get("/spices/")
    spices = res.json()
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    updated = next((s for s in spices if s["name"] == "Nutmeg"), None)
    assert updated
    assert "aromatic" in updated["flavor_profile"]


@pytest.mark.usefixtures("setup_test_dbs")
def test_link_and_unlink_spice():
    """Test linking and unlinking a spice to a recipe."""

    # Create a recipe
    recipe = {
        "name": "Apple Pie",
        "steps": "Bake apples and dough.",
        "ingredients": [
            {"name": "Apple", "quantity": 200, "unit": "Grm"},
            {"name": "Sugar", "quantity": 50, "unit": "Grm"},
        ],
    }
    res = client.post("/recipes/", json=recipe)
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert res.status_code == 201

    # Create a spice
    spice = {
        "name": "Cinnamon",
        "flavor_profile": "Warm and sweet",
        "recommended_quantity": "1 tsp per 500g",
        "pairs_with_ingredients": ["Apple"],
        "pairs_with_recipes": ["Apple Pie"],
    }
    res = client.post("/spices/", json=spice)
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert res.status_code == 201

    # Link spice to recipe
    link_data = {"spice_name": "Cinnamon", "recipe_name": "Apple Pie"}
    res = client.post("/spices/link", json=link_data)
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "success"

    # Unlink spice
    unlink_data = {"spice_name": "Cinnamon", "recipe_name": "Apple Pie"}
    res = client.post("/spices/unlink", json=unlink_data)
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"


@pytest.mark.usefixtures("setup_test_dbs")
def test_suggest_spices_for_recipe():
    """Test spice suggestion endpoint based on known recipe context."""
    # Create recipe first
    recipe = {
        "name": "Banana Bread",
        "steps": "Mash bananas, mix with flour, bake.",
        "ingredients": [
            {"name": "Banana", "quantity": 150, "unit": "Grm"},
            {"name": "Flour", "quantity": 200, "unit": "Grm"},
        ],
    }
    res = client.post("/recipes/", json=recipe)
    assert res.status_code == 201

    # Create relevant spice
    spice = {
        "name": "Cinnamon",
        "flavor_profile": "Warm and comforting",
        "recommended_quantity": "1 tsp per loaf",
        "pairs_with_ingredients": ["Banana", "Flour"],
        "pairs_with_recipes": ["Banana Bread"],
    }
    res = client.post("/spices/", json=spice)
    print("\n\nDEBUG RESPONSE:", res.json(), "\n\n") 
    assert res.status_code == 201

    # Suggest spices for the recipe
    res = client.get("/spices/suggest/Banana Bread")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert any("Cinnamon" in s["name"] for s in data)
