from fastapi import FastAPI
from app.core.modules.ingredients.routes_ingredients import router as ingredients_router
from app.core.modules.recipes.routes_recipes import router as recipes_router
from app.core.modules.spices.routes_spices import router as spices_router

app = FastAPI(
    title="PanaceIA API",
    description="A modular, AI-ready recipe management system 🍳",
    version="1.0.0"
)

app.include_router(ingredients_router)
app.include_router(recipes_router)
app.include_router(spices_router)


@app.get("/", tags=["root"])
def root():
    return {"message": "PanaceIA API is running successfully 🚀"}
