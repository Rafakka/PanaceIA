from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from app.core.db_manager import Base
import os


if "PYTEST_CURRENT_TEST" in os.environ:
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
    __tablename__ = "spices"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    flavor_profile = Column(String)
    recommended_quantity = Column(String)
    pairs_with_ingredients = Column(String)
    pairs_with_recipes = Column(String)
    
    recipe_links = relationship("RecipeSpice", back_populates="spice")
