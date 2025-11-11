import json

def test_import_single_spice(test_client):
    spice = {
        "name": "Cinnamon",
            "flavor_profile": "Warm and sweet",
            "recommended_quantity": "1 tsp per loaf",
            "pairs_with_ingredients": ["Banana", "Flour"],
            "pairs_with_recipes": ["Banana Cake", "Sweet Bread"]
    }

    res = test_client.post("/import/spice/", json=spice)
    assert res.status_code == 201
    assert res.json()["status"] == "success"

def test_import_bulk_spice(test_client):

    spices = [{
        "name": "Oregano",
            "flavor_profile": "Herbal and salty",
            "recommended_quantity": "1 tsp per kilo",
            "pairs_with_ingredients": ["Cheese", "Tomato"],
            "pairs_with_recipes": ["Pizza"]
    },{
        "name": "Tempero Baiano",
            "flavor_profile": "Spice and Eartly",
            "recommended_quantity": "1 tsp per kilo",
            "pairs_with_ingredients": ["Chicken", "Meat"],
            "pairs_with_recipes": ["Cooked Meat"]
    }, {
        "name": "Clover Leafs",
            "flavor_profile": "Herbal and mid",
            "recommended_quantity": "3 units per portion",
            "pairs_with_ingredients": ["Pasta", "Beans"],
            "pairs_with_recipes": ["Cooked Lentils"]
    }
    ]
    res = test_client.post("/import/bulkspices/", json=spices)
    assert res.status_code == 201
    for item in res.json():
        assert item["status"] == "success"
