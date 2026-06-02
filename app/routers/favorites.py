from fastapi import APIRouter, Depends, Request
from app.schema.recipe import RecipeTitleResponse
from app.schema.favorite import FavoriteResponse
from app.models.favorite import Favorite
from app.models.recipe import Recipe
from app.database import get_db, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, delete
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"] #Swaggerでのグループ名
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/",response_model=list[RecipeTitleResponse])
async def favorites(request:Request,db:Session = Depends(get_db)):
    user = request.session.get("user")
    
    favorite_recipe = (
        db.query(Favorite.id,Recipe.title)
        .join(Recipe,Favorite.recipe_id == Recipe.id)
        .all()
    )
    return templates.TemplateResponse(
        "favorites.html",
        {"request": request,
         "favorite": favorite_recipe,
         "user":user}
        
    )
#-- お気に入り追加 --
@router.post("/addition/{id}")
async def addition(id:int,request:Request,db:Session = Depends(get_db)):
    user = request.session.get("user")
    
    recipe = db.query(Recipe).filter(Recipe.id == id, Recipe.user == user).first()
    
    #-- すでにお気に入り済みか ---
    favorite = db.query(Favorite.recipe_id, Favorite.user).filter(Favorite.recipe_id == id, 
                                                                Favorite.user == user).first()
    #--　無ければ追加 ----
    if not favorite:
        favorite = Favorite(recipe_id = id, user=user)
        
        db.add(favorite)
        db.commit()
        db.refresh(favorite)

    
    return templates.TemplateResponse (
        "detail.html",
        {"request":request,
         "recipe":recipe,
         "is_favorites":True,
         "user":user}
    )
    

#-- お気に入り削除 -- 
@router.post("/{id}")
async def favorite_delete(id: int,request:Request, db:Session = Depends(get_db)):
    user = request.session.get("user")
    
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    
    #--　お気に入り済みか --
    favorite = db.query(Favorite.recipe_id).filter(Favorite.recipe_id == id).first()
    #-- あれば削除 --
    if favorite:
        Delete = delete(Favorite).where(Favorite.recipe_id == id )
    
        db.execute(Delete)
        db.commit()
    
    return templates.TemplateResponse (
        "detail.html",
        {"request":request,
         "recipe":recipe,
         "is_favorites":False,
         "user":user}
    )
 

