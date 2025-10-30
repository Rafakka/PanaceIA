from sqlalchemy import create_engine, Column, Engine, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///recipes.db", echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class RecipeIngredient(Base):
    __tablename__ ="recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id=Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Float)

    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient=relationship("Ingredient",back_populates="ingredient_recipes")

class Recipe(Base):
    __tablename__="recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    steps = Column(String)
    recipe_ingredients = relationship("RecipeIngredient", back_populates="ingredients")

class Ingredient(Base):
    __tablename__="ingredients"
        
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(String)
    ingredient_recipes = relationship("RecipeIngredient", back_populates="ingredients")


Base.metadata.create_all(bind=Engine)
