"""
Spices_models.py


Bridge between the main recipes DB and the spices DB.
Ensures both databases communicate correctly in tests and production.

"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from app.core.db_manager import Base
import os


if "PYTEST_CURRENT_TEST" in os.environ:
    """

    This condition check if its running test mode to set up a shared memory cache
    or use the local database for spices.

    """
    engine = create_engine(
        "sqlite:///file::memory:?cache=shared",
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        "sqlite:///spices.db",
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(bind=engine)

class Spice(Base):

    """
    
    This class especifies the variables a spice requires.

    Args:
    id: Identification number auto given to database
    name: The recipe's name
    - flavor_profile: short text describing its taste
        - recommended_quantity: e.g. "1 tsp per 500g meat"
        - pairs_with_ingredients: comma-separated list (stored as text)
        - pairs_with_recipes: comma-separated list (optional)
        
    """

    __tablename__ = "spices"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    flavor_profile = Column(String)
    recommended_quantity = Column(String)
    pairs_with_ingredients = Column(String)
    pairs_with_recipes = Column(String)
    
    recipe_links = relationship("RecipeSpice", back_populates="spice")
