from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import create_engine
from repositories import Recipe, RecipeCategory
from bs4 import BeautifulSoup
import requests

DATABASE_URI = "postgresql://postgres:89080620743@localhost:5432/FoodRecipe"
engine = create_engine(DATABASE_URI)

Base = declarative_base()
Base.metadata.create_all(engine)


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
            new_recipe = Recipe(
                name=recipe["name"],
                category_id=category.id,
                recipe_url=recipe["recipe_url"],
            )
            session.add(new_recipe)
    session.commit()


def scrape_recipes():
    url = "https://www.russianfood.com/recipes/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Находим список всех категорий рецептов на сайте
    tables = soup.find_all("table", {"class": "rcpf"})
    recipe_table = tables[0]

    # Находим все теги "a" внутри таблицы с рецептами
    recipe_links = recipe_table.find_all("a")

    # Список для хранения индексов заголовков с "Рецепты"
    header_indices = [0, 21, 85, 98, 131, 193, 202, 232, 234, 279]

    categories = []
    recipes = []

    # Проход по всем диапазонам индексов и создание категорий и рецептов
    for i in range(len(header_indices) - 1):
        category_name = recipe_links[header_indices[i]].text
        categories.append({"name": category_name})
        for link in recipe_links[header_indices[i] + 1 : header_indices[i + 1]]:
            link_text = link.text
            recipe_url = link.get("href")
            recipe = {
                "name": link_text,
                "category": category_name,
                "recipe_url": recipe_url,
            }
            recipes.append(recipe)

    return categories, recipes

def main():
    Base.metadata.create_all(engine)
    
    categories_data, recipes_data = scrape_recipes()
    
    with Session(engine, future=True) as session:
        processed_categories = add_categories(session, categories_data) # Заметьте, здесь вызываем add_categories с categories_data
        add_recipes(session, recipes_data, processed_categories) # Здесь вызываем add_recipes с recipes_data и processed_categories


if __name__ == "__main__":
    main()
