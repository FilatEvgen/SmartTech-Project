from bs4 import BeautifulSoup
import requests

def scrape_recipes():
    url = "https://www.russianfood.com/recipes/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Находим список всех тегов 'b'
    b_tags = soup.find_all('b')
    recipe_links = []
    category_markers_indices = []

    # По каждому тегу 'b', проверяем, содержит ли он слово 'Рецепты'
    # Если да, берем все 'a' теги, что идут после него, до следующего 'b' тега
    for tag_num, b_tag in enumerate(b_tags):
        if 'Рецепты' in b_tag.text:
            a_tags = []
            next_tag = b_tag.find_next_sibling()
            while next_tag and next_tag.name == 'a':
                a_tags.append(next_tag)
                next_tag = next_tag.find_next_sibling()

            recipe_links += a_tags
            category_markers_indices.append(len(recipe_links))
    
    categories = []
    recipes = []
    # Проход по всем диапазонам индексов и создание категорий и рецептов
 
    for i in range(len(category_markers_indices) - 1):
        category_name = recipe_links[category_markers_indices[i]].text
        categories.append({"name": category_name})
        for link in recipe_links[category_markers_indices[i] + 1 : category_markers_indices[i + 1]]:
            link_text = link.text
            recipe_url = link.get("href")
            recipe = {
                "name": link_text,
                "category": category_name,
                "recipe_url": recipe_url,
            }
            recipes.append(recipe)

    return categories, recipes
