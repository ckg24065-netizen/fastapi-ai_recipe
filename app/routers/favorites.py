from fastapi import APIRouter, Depends
from app.schema.recipe import RecipeTitleResponse
from app.schema.favorite import FavoriteResponse
from app.models.favorite import Favorite
from app.models.recipe import Recipe
from app.database import get_db, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"] #Swaggerでのグループ名
)

@router.get("/",response_model=list[RecipeTitleResponse])
async def favorites(db:Session = Depends(get_db)):
    
    favorite_recipe = (
        db.query(Favorite.id,Recipe.title)
        .join(Recipe,Favorite.recipe_id == Recipe.id)
        .all()
    )
    return favorite_recipe

@router.post("/",response_model=FavoriteResponse)
async def recipe(db:Session = Depends(get_db)):

    return {"id":1,"recipe_id":1,"created_at":"2025-11-20T00:00:00"}

@router.delete("/{id}")
async def delete(id: int, db:Session = Depends(get_db)):
    """
    お気に入り削除
    """
    return {"status":204,"detail":"favorite delete"}
 
# ---- テストデータ -----   
@router.get("/test-favorite")
def test_favorite(db: Session = Depends(get_db)):

    new_favorite = Favorite(recipe_id=1)
    recipe = db.query(Recipe).filter(Recipe.id == 1).first()
    db.add(new_favorite)
    db.commit()

    return {
        "title": recipe.title,
        "material":recipe.material,
        "recipe_text":recipe.recipe_text
    }
