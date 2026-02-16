from fastapi import APIRouter
from app.schema.recipe import RecipeCreate,RecipeResponse,RecipeTitleResponse

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"] #Swaggerでのグループ名
)

#-----------------------
#レシピ生成に対しての動き
#-----------------------

#----好みや材料入力ページの動き---
@router.post("/")
async def create_recipe(recipe: RecipeCreate):
    """
    料理に対しての好みを入力動き
    """
    return{
        "title":"料理名",
        "material": "材料",
        "recipe_text": "レシピ",
        "genre": "主食か副菜か",
        "category": "カテゴリー"}
    
    
#----レシピ生成4つ-----
@router.post("/generate",response_model=list[RecipeResponse])
async def generation_recipe():
    """
    AIにレシピ生成
    """
    return[ 
        {"id":1,"title": "料理名","material": "材料","recipe_text": "材料","genre": "主食","category": "和食","created_at": "2025-11-20T00:00:00"},
        {"id":2,"title": "料理名","material": "材料","recipe_text": "材料","genre": "主食","category": "和食","created_at": "2025-11-20T00:00:00"},
        {"id":3,"title": "料理名","material": "材料","recipe_text": "材料","genre": "主食","category": "和食","created_at": "2025-11-20T00:00:00"},
        {"id":4,"title": "料理名","material": "材料","recipe_text": "材料","genre": "主食","category": "和食","created_at": "2025-11-20T00:00:00"},
    ]

#-----------------
#履歴に対しての動き
#-----------------

#----料理一覧画面-----
@router.get("/",response_model=list[RecipeTitleResponse])
async def history():
    """
    DBから料理名の一覧を表示
    """
    return[
        {"id":1,"title":"料理名"}
    ]

#----料理詳細ページ----
@router.get("/recipe/{id}",response_model=RecipeResponse)
async def recipe(id:int):
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