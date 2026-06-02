from pydantic import BaseModel
from datetime import datetime 

class RecipeBase(BaseModel):
    title: str
    material: str
    recipe_text:str
    genre: str
    category: str

class RecipeCreate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):  
    id: int
    created_at: datetime

class RecipeTitleResponse(BaseModel):
    id:int
    title:str

class RecipeFromGemini(RecipeBase):
    pass

class Recipeuserinput(BaseModel):
    material: str
    genre: str
    category: str
    volume: str | None = None
    taste: str | None = None

class Recipedetail(BaseModel):
    title: str
    material: str
    recipe_text:str
    genre: str
    category: str
