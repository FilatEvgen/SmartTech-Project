from sqlalchemy import Column, Integer, String, ForeignKey,Text
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
    __tablename__ = "recipe_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    dishes = relationship("TypeofDish", back_populates="category")


class TypeofDish(Base):
    __tablename__ = "type_of_dishes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    recipe_url = Column(String)
    category_id = Column(Integer, ForeignKey("recipe_categories.id"))

    category = relationship("RecipeCategory", back_populates="dishes")


class UserRecipe(Base):
    __tablename__ = 'user_recipes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # связь с таблицей пользователей
    name = Column(String)
    ingredients = Column(String)
    steps = Column(Text)
    image_url = Column(String)

    user = relationship('User')  # связь с моделью User


