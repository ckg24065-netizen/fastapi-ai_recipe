from app.database import engine
from app.models.recipe import Recipe
from app.models.favorite import Favorite
from app.database import Base


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("DB initialized.")