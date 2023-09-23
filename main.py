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
    for category in categories:
        new_category = RecipeCategory(name=category["name"])
        session.add(new_category)
    session.commit()

def add_recipes(session, recipes):
    for recipe in recipes:
        new_recipe = Recipe(
            name=recipe["name"],
            category=recipe["category"],
            recipe_url=recipe["recipe_url"]
        )
        session.add(new_recipe)
    session.commit()

def scrape_recipes():
    url = "https://www.russianfood.com/recipes/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    recipe_links = soup.find_all("a") # Получение всех ссылок на странице, замените эту строку кода собственным кодом, который будет извлекать ссылки на рецепты и категории.

    # Заменим вызовы print на заполнение списков
    category_links = soup.find_all('table', {'class': 'rcpf'})
    recipe_links = soup.find_all("a", class_="recipe-class") 
    for i in range(len(header_indices)-1):
        for link in recipe_links[header_indices[i]+1:header_indices[i+1]]:
            link_text = link.text
            print(f'Текст ссылки: {link_text}')
            print(f'URL: {link.get("href")}')
            print('---')

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
    # Создание сессии
    Session = sessionmaker(bind=engine)
    session = Session()

    # Получение и добавление категорий и рецептов
    categories, recipes = scrape_recipes()
    add_categories(session, categories)
    add_recipes(session, recipes)

    session.close()  # Закрытие сессии

if __name__ == "__main__":
    main()
