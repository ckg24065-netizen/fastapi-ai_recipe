from fastapi import APIRouter, Depends
from fastapi import Request, Form
from fastapi.responses import (HTMLResponse,
                               RedirectResponse)
from fastapi.templating import Jinja2Templates
from app.models.recipe import Recipe
from app.models.favorite import Favorite
from app.schema.recipe import (RecipeTitleResponse,
                               RecipeFromGemini,
                               Recipeuserinput,
                               Recipedetail)
from app.services.gemini import gemini
from app.database import get_db
from sqlalchemy.orm import Session 
from typing import Optional

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"] #Swaggerでのグループ名
)

templates = Jinja2Templates(directory="app/templates")

#-------------------
#--- ログイン機能 ---
#-------------------
@router.get("/login")
async def login_top(request:Request):
    return templates.TemplateResponse(
        "login.html",
        {"request":request}
    )
#ログイン判断
@router.post("/login-after")
async def login(
    request:Request,
    user_name: str = Form(...),
    password: str = Form(...),):

    users={
        
        "nozomi": "1012",
        "airi": "0416",
        "rui": "0601",
        "rutonn": "0817",
        "guest" : "0000"
    }
    
    if user_name in users:
        if users[user_name] == password:
            
            request.session["user"] = user_name
            return RedirectResponse(url="/recipes/top",status_code=303)
            
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request":request,
                 "message":"パスワードが違います",
                 "username":user_name}
            )
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request":request,
             "message":"ユーザーネームが違います",
             "username":user_name}
        )
#--- ログアウト ---
@router.get("/logout")
async def logout(request:Request):
    request.session.clear()
    return RedirectResponse("/recipes/login")

#----- トップページ -----
@router.get("/top")
async def top(request:Request):
    user = request.session.get("user")
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "user":user}
    )
#--- ユーザー入力 ---       
@router.get("/create", response_class=HTMLResponse)
async def create(request: Request):
    
    return templates.TemplateResponse(
        "select.html",
        {"request": request}
    )

#-------------------------------
#---- レシピ生成に対しての動き ---
#-------------------------------

#--- 入力後のローディング ---
@router.post("/loading")
async def loading(
    request: Request,
    category: str = Form(...),
    genre: str = Form(...),
    taste: Optional[str] = Form(None),
    volume: Optional[str] = Form(None),
    material: str = Form(...)):
    
    user = request.session.get("user")
    
    if user is None:
        return RedirectResponse("/recipes/login", status_code=302)
    
    return templates.TemplateResponse(
        "loading.html",
        {"request": request,
         "category":category,
         "genre":genre,
         "taste":taste,
         "volume":volume,
         "material":material}
    ) 

#---- 好みや材料入力 ---
@router.post("/generate", response_model=list[Recipeuserinput])
async def create_recipe(
    request:Request,
    db:Session = Depends(get_db),
    category: str = Form(...),
    genre: str = Form(...),
    taste: Optional[str] = Form(None),
    volume: Optional[str] = Form(None),
    material: str = Form(...)):
    
    vlidated = Recipeuserinput(
    category=category,
    genre=genre,
    taste=taste,
    volume=volume,
    material=material
    )
    recipes = await gemini(vlidated)
    user = request.session.get("user")
    
    if recipes is None:
        
        return templates.TemplateResponse(
            "error.html",
            {"request": request,
             "category":category,
             "genre":genre,
             "taste":taste,
             "volume":volume,
             "material":material}
        )
    
    for data in recipes["recipes"]:
        validated = RecipeFromGemini(**data)

        new_recipe = Recipe(**validated.dict(),user=user)
        
        db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return templates.TemplateResponse(
        "generate.html",
        {"request": request,
        "recipe": new_recipe}
        
    )
    
#--------------------------
#---- 履歴に対しての動き ----
#--------------------------

#----料理一覧画面-----
@router.get("/history",response_model=list[RecipeTitleResponse])
async def history(request:Request,db:Session = Depends(get_db),):
    user = request.session.get("user")

    recipes = db.query(Recipe.id,
                      Recipe.title,
                      Recipe.user).filter(Recipe.user == user).all()
    return templates.TemplateResponse(
        "history.html",
        {"request": request,
         "recipes":recipes,
         "user":user}
    )

#----料理詳細ページ----
@router.get("/recipe/{id}",response_model=list[Recipedetail])
async def recipe(request:Request,id:int, db:Session = Depends(get_db)):
    user = request.session.get("user")
    
    recipe = db.query(Recipe).filter(Recipe.id == id).first()

    favorite = db.query(Favorite.recipe_id).filter(Favorite.recipe_id == id).first()
        
    is_favorites = favorite is not None
    
    return templates.TemplateResponse (
        "detail.html",
        {"request":request,
         "recipe":recipe,
         "is_favorites":is_favorites,
         "user":user}
    )