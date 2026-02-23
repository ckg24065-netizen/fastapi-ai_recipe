from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(64), nullable=False)
    material = Column(Text, nullable=False)
    recipe_text = Column(Text, nullable=False)
    genre = Column(String(64), nullable=False)
    category = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    