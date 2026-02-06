from fastapi import APIRouter

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"] #Swaggerでのグループ名
)