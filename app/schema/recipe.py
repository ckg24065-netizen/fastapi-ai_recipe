from pydantic import BaseModel

class recipeBase(BaseModel):
    title: str
    material: str
    recipe: str

class 