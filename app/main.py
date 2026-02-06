from fastapi import FastAPI
from app.routers import recipes
from app.routers import favorites

app = FastAPI(title="RECIPES API - step1")

#recipesルーターを登録
app.include_router(recipes.router)

#favoritesルーターを登録
app.include_router(favorites.router)
