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

#    
class RecipeTitleResponse(BaseModel):
    id:int
    title:str