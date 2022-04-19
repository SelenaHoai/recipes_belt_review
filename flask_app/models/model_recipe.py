from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user

from flask_app import DATABASE, bcrypt

from flask import flash, session
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.time = data['time']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @property
    def user_actual(self):
        return model_user.User.get_one({'id': self.user_id})


    @classmethod
    def save(cls, data):
        query = "INSERT into recipes (name,description,instruction,user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

# C
    @classmethod
    def create(cls, data: dict) -> int:
        query = "INSERT INTO recipes (name, description, instruction, time, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(time)s, %(user_id)s)"
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        return user_id

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)


# R
    @classmethod
    def get_all_recipes(cls,data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if results: 
            all_recipes = []
            for recipe in results:
                recipe_actual = cls(recipe)

                data = {
                    'id': recipe['users.id'],
                    'first_name': recipe['first_name'],
                    'last_name': recipe['last_name'],
                    'email': recipe['email'],
                    'password': recipe['password'],
                    'created_at': recipe['users.created_at'],
                    'updated_at': recipe['users.updated_at'],
                }

                owner = model_user.User(data)
                recipe_actual.owner = owner

                all_recipes.append(recipe_actual)
            return all_recipes
        return []

    @classmethod
    def update_one_recipe(cls, data: dict) -> object:
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, time=%(time)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    @classmethod
    def delete_recipe(cls, data: dict) -> object:
        query = "DELETE FROM recipes WHERE id = (%(id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
        