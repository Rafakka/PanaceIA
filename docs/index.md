🧠 PanaceIA — Intelligent Recipe Management System
🍳 Overview

PanaceIA is a modular, intelligent recipe management application that learns user preferences and adapts its suggestions over time.
Built with FastAPI, SQLAlchemy, and Pydantic, the system allows users to add, organize, and refine recipes while maintaining clean, validated data.

PanaceIA’s architecture was designed for scalability and intelligence — from the database layer to the API endpoints — allowing future integration of machine learning models for automatic recipe recommendations and ingredient substitutions.

⚙️ Core Features

🧩 Modular Architecture — Clear separation of concerns across core, modules, and database layers.

🍲 Recipe & Ingredient Management — Full CRUD operations for both entities.

🧼 Data Cleaning Pipeline — Automatic normalization of strings, quantities, and measurement units before database storage.

🧠 Validation with Pydantic — Strict schema enforcement ensures robust and predictable input handling.

⚡ RESTful API with FastAPI — Lightweight, fast, and ready for integration with mobile and web frontends.

🔐 Database Persistence — Built on SQLite for local use, easily extendable to PostgreSQL or MySQL.

🤖 AI-Ready Foundation — Future modules can include natural language recipe generation and personalized taste learning.

🧱 System Architecture

PanaceIA is divided into independent yet connected layers:
    ```
    app/
    │
    ├── core/
    │   ├── db_manager.py        # SQLAlchemy ORM and database setup
    │   ├── data_cleaner.py      # Validation and normalization pipeline
    │   ├── schemas.py           # Pydantic models for strict type validation
    │   ├── recommender.py       # Placeholder for future AI logic
    │   └── modules/
    │       ├── ingredients/
    │       │   ├── ingredients_manager.py
    │       │   └── routes_ingredients.py
    │       └── recipes/
    │           ├── recipes_manager.py
    │           └── routes_recipes.py
    │
    ├── database/
    │   └── recipes.db
    │
    └── tests/
        ├── test_api_recipe.py
        └── test_data_cleaner.py
    ```
Each module is designed to work independently while maintaining consistent input/output patterns through shared cleaning and validation utilities.

🧩 Technology Stack

Layer	Technology	Purpose
Backend Framework	FastAPI	RESTful API architecture
Database ORM	SQLAlchemy	Data persistence and relations
Validation Layer	Pydantic	Schema enforcement and input safety
Data Cleaning	Custom pipeline	Consistent normalization and sanitation
Documentation	MkDocs + mkdocstrings	Auto-generated, developer-friendly docs
Testing	Requests + CLI tests	Endpoint and logic verification

🤖 Future Enhancements

🧮 AI-Powered Recommendation Engine — Suggest recipes based on ingredient availability and taste preferences.

🧠 Substitution System — Dynamically replace ingredients using embeddings or similarity scoring.

📱 Mobile Integration — Kotlin client consuming the FastAPI endpoints.

📊 Usage Analytics — Track popular ingredients and recipes for adaptive recommendations.

🧬 Philosophy

PanaceIA takes inspiration from the world PANACEA, which mean healing thru food.
Every module, every layer, every normalization step reflects this ethos:
transforming scattered user input into refined, meaningful information.

✍️ Author

Rafael Kaher
Developer · Architect · Eternal Student

“Code should not just work — it should evolve.”