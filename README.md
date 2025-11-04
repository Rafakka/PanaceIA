<p align="center">
<img width="500" height="500" alt="paneacia_gitpage" src="https://github.com/user-attachments/assets/a11caa97-5166-4440-b1a6-a31d0dfe8670" />
</p>

🧠 PanaceIA — Intelligent Recipe Management System

**PanaceIA** is a modular, intelligent recipe management app that learns user preferences and adapts its suggestions over time.  
Built with **FastAPI**, **SQLAlchemy**, and **Pydantic**, it offers a clean data pipeline, strict validation, and a future-ready foundation for AI-driven recipe recommendations.

---

## ⚙️ Features

- 🍲 **Full Recipe & Ingredient CRUD** — Manage recipes and ingredients seamlessly.
- 🧼 **Data Cleaning Pipeline** — Automatic normalization for safe and consistent input.
- 🧠 **Strict Validation** — Pydantic schemas enforce structure and data integrity.
- ⚡ **RESTful API** — FastAPI backend ready for mobile or web integration.
- 🧩 **Modular Design** — Clean architecture ready for AI recommendation modules.

---

## 🧱 Architecture Overview

```
app/
├── core/
│   ├── db_manager.py          # ORM & DB setup
│   ├── data_cleaner.py        # Input normalization
│   ├── schemas.py             # Validation models
│   ├── recommender.py         # AI placeholder
│   └── modules/
│       ├── ingredients/
│       │   ├── ingredients_manager.py
│       │   └── routes_ingredients.py
│       └── recipes/
│           ├── recipes_manager.py
│           └── routes_recipes.py
├── database/
│   └── recipes.db
└── tests/
    ├── test_api_recipe.py
    └── test_data_cleaner.py
```

---

## 🤖 Future Plans

- 🧮 AI-powered recipe recommendations  
- 🔄 Smart ingredient substitutions  
- 📱 Kotlin mobile integration  
- 📊 Usage analytics and trend insights  

---

## 🌿 Philosophy

The name **PanaceIA** honors *Panacea*, the goddess of the universal remedy — the divine embodiment of healing through nourishment.  
This system carries her legacy into the digital age, guided by the belief that **eating itself is the universal cure** — a sacred act where health, knowledge, and pleasure intertwine.

Food is both *prevention* and *remedy*, and PanaceIA stands as the bridge between code and care, science and soul —  
a tool that helps transform ingredients into balance, data into vitality, and recipes into acts of healing.

---

## ✍️ Author

**Rafael Kaher**  
_Developer · Architect · Eternal Student_  
> “Code should not just work — it should *evolve*.”
