from fastapi import APIRouter

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"] #Swaggerでのグループ名
)

#-----レシピ生成に対しての動き-----
@router.get("/")
async def create_recipe():
    """
    料理に対しての好みを入力動き
    """
    return[
        {"message":"好み入力"},
    ]

@router.post("/generations")
async def generation_recipe():
    """
    AIにレシピ生成
    """
    return {"status":"ok","message":"仮作成"}


#----履歴に対しての動き-----
@router.get("/recipes{id}")
async def history():
    """
    DBから料理名の一覧を表示
    """
    return[
        {"message":"料理名"}
    ]

@router.get("/recipe{id}")
async def recipe():
    """
    履歴のレシピ詳細閲覧ページ

    """
    return[
        {"message":"料理名"},
        {"message":"材料"},
        {"message":"レシピ"},
    ]