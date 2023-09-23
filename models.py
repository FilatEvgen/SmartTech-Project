from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    vk_id = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    image_url = Column(String)


class RecipeCategory(Base):
    __tablename__ = 'recipe_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)  # название категории рецепта


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey('recipe_categories.id'))  # связь с таблицей категорий рецептов
    ingredients = Column(String)
    steps = Column(String)
    image_url = Column(String)
    recipe_url = Column(String)

    category = relationship('RecipeCategory')  # связь с моделью RecipeCategory


class UserRecipe(Base):
    __tablename__ = 'user_recipes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # связь с таблицей пользователей
    name = Column(String)
    ingredients = Column(String)
    steps = Column(Text)
    image_url = Column(String)

    user = relationship('User')  # связь с моделью User


def main():
    # подключение к базе данных
    database_url = 'postgresql://postgres:89080620743@localhost:5432/RussianFoodRecipe'
    engine = create_engine(database_url)

    Base.metadata.create_all(engine)  # Создание таблиц
    # Base.metadata.drop_all(engine)  # Удаление таблиц

if __name__ == '__main__':
    main()  # запуск основной функции