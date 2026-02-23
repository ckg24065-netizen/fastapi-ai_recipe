from fastapi import APIRouter, Depends
from app.models.recipe import Recipe
from app.schema.recipe import RecipeCreate,RecipeResponse,RecipeTitleResponse, RecipeFromGemini
from app.services.gemini import gemini
from app.database import get_db
from sqlalchemy.orm import Session 
from sqlalchemy import select, insert
import os

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"] #Swaggerでのグループ名
)
print(os.getenv("GOOGLE_API_KEY"))
#-----------------------
#レシピ生成に対しての動き
#-----------------------

#----好みや材料入力ページの動き---
@router.post("/generate")
async def create_recipe(recipe: RecipeCreate, db:Session = Depends(get_db)):

    result = await gemini(recipe.material)
    
    for data in result["recipes"]:
        validated = RecipeFromGemini(**data)

        new_recipe = Recipe(**validated.dict())
        
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

#----レシピ生成4つ-----下記のapiが不必要だと判断
"""
@router.post("/generate",response_model=list[RecipeResponse])
async def generation_recipe(recipe:RecipeCreate, db:Session = Depends(get_db)):
    
    
    db.add(generate_recipe)
    db.commit()
    db.refresh()
    return[ 
        {"id":1,"title": "料理名","material": "材料","recipe_text": "材料","genre": "主食","category": "和食","created_at": "2025-11-20T00:00:00"},
        {"id":2,"title": "料理名","material": "材料","recipe_text": "材料","genre": "主食","category": "和食","created_at": "2025-11-20T00:00:00"},
        {"id":3,"title": "料理名","material": "材料","recipe_text": "材料","genre": "主食","category": "和食","created_at": "2025-11-20T00:00:00"},
        {"id":4,"title": "料理名","material": "材料","recipe_text": "材料","genre": "主食","category": "和食","created_at": "2025-11-20T00:00:00"},
    ]
"""

#-----------------
#履歴に対しての動き
#-----------------

#----料理一覧画面-----
@router.get("/",response_model=list[RecipeTitleResponse])
async def history(db:Session = Depends(get_db)):
    """
    DBから料理名の一覧を表示
    """
    return[
        {"id":1,"title":"料理名"}
    ]

#----料理詳細ページ----
@router.get("/recipe/{id}",response_model=RecipeResponse)
async def recipe(id:int, db:Session = Depends(get_db)):
    """
    履歴のレシピ詳細

    """
    return {
        "id": 1,
        "title": "料理名",
        "material": "材料",
        "recipe_text": "材料",
        "genre": "主食",
        "category": "和食",
        "created_at": "2025-11-20T00:00:00",
    }