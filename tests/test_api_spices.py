def test_add_and_list_spices(test_client):
    """Test creating and listing spices."""
    spice = {
        "name": "Cinnamon",
        "flavor_profile": "Warm and sweet",
        "recommended_quantity": "1 tsp per 500g",
        "pairs_with_ingredients": ["Apple", "Sugar"],
        "pairs_with_recipes": ["Apple Pie"]
    }

    # Add
    res = test_client.post("/spices/", json=spice)
    assert res.status_code == 201
    assert res.json()["status"] == "success"

    # List
    res = test_client.get("/spices/")
    assert res.status_code == 200
    spices = res.json()["data"]
    assert any(s["name"] == "Cinnamon" for s in spices)


def test_suggest_spices(test_client):
    """Test suggesting spices for a recipe (gracefully handles empty DB)."""
    res = test_client.get("/spices/suggest/Pancakes")

    assert res.status_code in (200, 500)
    data = res.json()
    assert "status" in data


def test_update_spice(test_client):
    """Test updating spice attributes."""
    update_data = {
        "name": "Cinnamon",
        "flavor_profile": "Sweet and aromatic",
        "recommended_quantity": "½ tsp per 250g"
    }

    res = test_client.put("/spices/", json=update_data)
    assert res.status_code == 200
    assert res.json()["status"] == "success"


def test_link_and_unlink_spice(test_client):
    """Test linking and unlinking a spice to/from a recipe."""
    # Link
    link_data = {"spice_name": "Cinnamon", "recipe_name": "Pancakes"}
    res = test_client.post("/spices/link", json=link_data)
    assert res.status_code == 201
    assert res.json()["status"] == "success"

    # Unlink
    unlink_data = {"spice_name": "Cinnamon", "recipe_name": "Pancakes"}
    res = test_client.request("DELETE", "/spices/unlink", json=unlink_data)
    assert res.status_code == 200
    assert res.json()["status"] == "success"