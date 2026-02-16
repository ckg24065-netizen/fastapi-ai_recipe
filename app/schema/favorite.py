from pydantic import BaseModel
from datetime import datetime 

class FavoriteBase(BaseModel):
    recipe_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):  
    id: int 
    created_at: datetime

 