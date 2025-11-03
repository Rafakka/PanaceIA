import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/recipes"

# Helper to print responses nicely
def show(title, res):
    print(f"\n🔹 {title}")
    print(f"➡️ Status: {res.status_code}")
    try:
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    except Exception:
        print("No JSON response or parse error.")
    time.sleep(0.3)  # Small pause for readability


def test_recipes():
    # 1️⃣ Add new recipe
    recipe_data = {
        "name": "Pancakes",
        "steps": "Mix ingredients and fry until golden.",
        "ingredients": [
            {"name": "Flour", "quantity": 200, "unit": "g"},
            {"name": "Milk", "quantity": 250, "unit": "ml"},
            {"name": "Egg", "quantity": 2, "unit": "pcs"}
        ]
    }

    res = requests.post(f"{BASE_URL}/", json=recipe_data)
    show("Create Recipe", res)

    # 2️⃣ List all recipes
    res = requests.get(f"{BASE_URL}/")
    show("List Recipes", res)

    # 3️⃣ Get recipe by name
    res = requests.get(f"{BASE_URL}/Pancakes")
    show("Get Recipe by Name", res)

    # 4️⃣ Update recipe name
    update_name_data = {"old_name": "Pancakes", "new_name": "Fluffy Pancakes"}
    res = requests.put(f"{BASE_URL}/name", json=update_name_data)
    show("Update Recipe Name", res)

    # 5️⃣ Update ingredient quantity
    update_quantity_data = {
        "recipe_name": "Fluffy Pancakes",
        "ingredient": "Flour",
        "new_quantity": 250
    }
    res = requests.put(f"{BASE_URL}/quantity", json=update_quantity_data)
    show("Update Ingredient Quantity", res)

    # 6️⃣ Remove ingredient from recipe
    remove_ing_data = {"name": "Fluffy Pancakes", "ingredient": "Egg"}
    res = requests.delete(f"{BASE_URL}/ingredient", json=remove_ing_data)
    show("Remove Ingredient from Recipe", res)

    # 7️⃣ Delete recipe
    delete_data = {"name": "Fluffy Pancakes"}
    res = requests.delete(f"{BASE_URL}/", json=delete_data)
    show("Delete Recipe", res)


if __name__ == "__main__":
    print("🚀 Starting Recipe API tests...")
    test_recipes()
    print("\n✅ All test requests completed. Check responses above.")
