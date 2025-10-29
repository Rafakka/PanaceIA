from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Engine, Integer, String, Float

engine = create_engine("sqlite:///recipes.db", echo=True)

Base = declarative_base()

class Ingredient(Base):
    __tablename__="ingredients"
        
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    quantity = Column (Float, default=0)
    unit = Column(String)

    def __repr__(self):
        return f"<Ingredient(name='{self.name}',qty={self.quantity},unit='{self.unit})>"

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=Engine)
