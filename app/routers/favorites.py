from fastapi import APIRouter, Depends
from app.schema.recipe import RecipeResponse,RecipeTitleResponse
from app.schema.favorite import FavoriteCreate,FavoriteResponse
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"] #Swaggerでのグループ名
)

@router.get("/",response_model=list[RecipeTitleResponse])
async def favorites(db:Session = Depends(get_db)):
    """
    お気に入り閲覧
    """
    return [
        {"id":1,"title":"料理名"}
    ]

@router.post("/",response_model=FavoriteResponse)
async def recipe(db:Session = Depends(get_db)):
    """
    お気に入り追加
    """
    return {"id":1,"recipe_id":1,"created_at":"2025-11-20T00:00:00"}

@router.delete("/{id}")
async def delete(id: int, db:Session = Depends(get_db)):
    """
    お気に入り削除
    """
    return {"status":204,"detail":"favorite delete"}
    
