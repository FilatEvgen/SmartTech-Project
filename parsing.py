from bs4 import BeautifulSoup
import requests

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

