from fastapi import APIRouter

router = APIRouter(
    prefix="/favorites",
    tags=["Favorites"] #Swaggerでのグループ名
)

@router.get("favorites")
async def favorites():
    """
    generationで登録されたレシピを一覧表示
    DBから情報を持ってくる
    """
    return{"message":"お気に入り登録一覧"}

@router.get("/favorite{id}")
async def recipe():
    """
    お気に入りのレシピ詳細閲覧ページ

    """
    return[
        {"message":"料理名"},
        {"message":"材料"},
        {"message":"作り方"},
    ]