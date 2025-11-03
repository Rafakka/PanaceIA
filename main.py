from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes_ingredients import router as ingredients_router
from routes_recipes import router as recipes_router

app = FastAPI(
    title="PanaceIA Recipe API",
    description="Smart recipe management API that learns your tastes.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingredients_router)
app.include_router(recipes_router)

@app.get("/")
def root():
    return {"message": "PanaceIA API is running successfully 🚀"}
