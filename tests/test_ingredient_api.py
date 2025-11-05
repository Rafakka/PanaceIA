def test_add_and_list_ingredients(test_client):
    ingredient = {"name": "Eggs", "quantity": 2, "unit": "Unit"}
    res = test_client.post("/ingredients/", json=ingredient)
    assert res.status_code == 201
    assert res.json()["status"] == "success"

    res = test_client.get("/ingredients/")
    assert res.status_code == 200
    assert any(i["name"] == "Eggs" for i in res.json())

def test_update_and_delete_ingredient(test_client):

    test_client.post("/ingredients/", json={"name": "Milk", "quantity": 1, "unit": "L"})

    res = test_client.put("/ingredients/name", json={"old_name": "Milk", "new_name": "Oat Milk"})
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    res = test_client.request("DELETE", "/ingredients/", json={"name": "Oat Milk"})
    assert res.status_code == 200
    assert res.json()["status"] == "success"
