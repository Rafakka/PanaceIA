from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///app/core/modules/spices/db/spices.db", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Spice(Base):
    __tablename__ = "spices"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    flavor_profile = Column(String)
    recommended_quantity = Column(String)
    pairs_with_ingredients = Column(String)
    pairs_with_recipes = Column(String)

Base.metadata.create_all(bind=engine)
