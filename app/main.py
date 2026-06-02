from fastapi import FastAPI
from app.routers import recipes
from app.routers import favorites
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI(title="RECIPES API - step1")

app.add_middleware(
    SessionMiddleware,
    secret_key="test_secret-1234"
)

#recipesルーターを登録
app.include_router(recipes.router)

#favoritesルーターを登録
app.include_router(favorites.router)

