from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, RecipeCategory, TypeofDish
from repositories import add_categories, add_recipes
from parsing import scrape_recipes

DATABASE_URI = "postgresql://postgres:89080620743@localhost:5432/FoodRecipe"
engine = create_engine(DATABASE_URI)

def main():
    Base.metadata.create_all(engine)
    
    categories_data, recipes_data = scrape_recipes()

    with Session(engine, future=True) as session:
        processed_categories = add_categories(session, categories_data)
        add_recipes(session, recipes_data, processed_categories)

if __name__ == "__main__":
    main()