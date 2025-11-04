"""
db_manager.py

Defines the SQLAlchemy ORM models and database engine configuration
used across the system.

This module establishes the relational structure between recipes and ingredients,
providing persistent storage and standardized access to the database layer.

Author: Rafael Kaher

"""


from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("sqlite:///app/database/recipes.db", echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class RecipeIngredient(Base):

    """
    Represents the association table linking recipes and ingredients.
    Each record defines the quantity of a specific ingredient used in a recipe.

    Args:
        recipe_id (int): Foreign key referencing the recipe.
        ingredient_id (int): Foreign key referencing the ingredient.
        quantity (float): The amount of the ingredient used in the recipe.

    Relationships:
        recipe: Bidirectional link to the parent Recipe object.
        ingredient: Bidirectional link to the associated Ingredient object.

    Example:
        ```python
        link = RecipeIngredient(recipe_id=1, ingredient_id=2, quantity=250.0)
        session.add(link)
        ```
    """

    __tablename__ = "recipe_ingredients"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True)
    quantity = Column(Float)

    recipe = relationship("Recipe", back_populates="recipe_ingredients")
    ingredient = relationship("Ingredient", back_populates="ingredient_recipes")

class Recipe(Base):
    """
    Represents a recipe entity in the system.
    Each recipe has a unique name, preparation steps,
    and one or more linked ingredients through the RecipeIngredient relationship.
    
    Args:
        id (int): Primary key identifier.
        name (str): Recipe name, must be unique.
        steps (str): Instructions for preparation.

    Relationships:
        recipe_ingredients: A list of RecipeIngredient objects linked to this recipe.

    Example:
        ```python
        new_recipe = Recipe(name="Pancakes", steps="Mix and fry until golden.")
        session.add(new_recipe)
        ```
    """
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    steps = Column(String)

    recipe_ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

class Ingredient(Base):
    """
    Represents an ingredient entity in the database.
    Each ingredient can be associated with one or more recipes.

    Attributes:

        id (int): Primary key identifier.
        name (str): Ingredient name, must be unique.
        unit (str): Measurement unit, such as "Grm" or "Mls".

    Relationships:

        ingredient_recipes: A list of RecipeIngredient objects linking this ingredient to recipes.

    Example:
        ```python
        new_ingredient = Ingredient(name="Flour", unit="Grm")
        session.add(new_ingredient)
        ```
    """

    new_ingredient = Ingredient(name="Flour", unit="Grm")
    session.add(new_ingredient)
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    unit = Column(String)

    ingredient_recipes = relationship(
        "RecipeIngredient",
        back_populates="ingredient"
    )

class Spice(Base):
    """
    Represents a spice in the system.
    Stored independently from ingredients to allow flexible linking and suggestions.
    """
    __tablename__ = "spices"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    flavor_profile = Column(String, nullable=True)

    recipe_links = relationship("RecipeSpice", back_populates="spice")


class RecipeSpice(Base):
    """
    Association table linking recipes and spices.
    Each record indicates that a recipe includes or was suggested a given spice.
    """
    __tablename__ = "recipe_spices"

    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    spice_id = Column(Integer, ForeignKey("spices.id"), primary_key=True)

    recipe = relationship("Recipe", back_populates="spice_links")
    spice = relationship("Spice", back_populates="recipe_links")


Recipe.spice_links = relationship(
    "RecipeSpice", back_populates="recipe", cascade="all, delete-orphan"
)

Base.metadata.create_all(bind=engine)
