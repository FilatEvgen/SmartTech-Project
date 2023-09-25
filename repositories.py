from sqlalchemy.orm import Session
from models import RecipeCategory,TypeofDish
from sqlalchemy import create_engine

DATABASE_URI = "postgresql://postgres:89080620743@localhost:5432/FoodRecipe"
engine = create_engine(DATABASE_URI)

def add_categories(session, categories):
    processed_categories = []
    for category in categories:
        new_category = RecipeCategory(name=category["name"])
        session.add(new_category)
        processed_categories.append(new_category)
    session.flush()  # Обновление сессии, чтобы получить id новых категорий
    return processed_categories

def add_recipes(session, recipes, categories):
    for recipe in recipes:
        category = next((c for c in categories if c.name == recipe["category"]), None)
        if category:
            new_dish = TypeofDish(
                name=recipe["name"],
                category_id=category.id,
                recipe_url=recipe["recipe_url"],
            )
            session.add(new_dish)
    session.commit()

   