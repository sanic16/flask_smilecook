from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe

from flask_jwt_extended import get_jwt_identity, jwt_required

class RecipeListResource(Resource):
    def get(self):
        recipes = Recipe.get_all_published()
        data = [recipe.data() for recipe in recipes]
        return {'data': data}, HTTPStatus.OK
    
    @jwt_required(optional=False)
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        recipe = Recipe()
        recipe.name = json_data['name']
        recipe.description = json_data['description']
        recipe.num_of_servings = json_data['num_of_servings']
        recipe.cook_time = json_data.get('cook_time')
        recipe.directions = json_data.get('directions')
        recipe.user_id = current_user

        recipe.save()
        return recipe.data(), HTTPStatus.CREATED


    
class RecipeResource(Resource):
    @jwt_required(optional=True)
    def get(self, recipe_id):
        recipe = Recipe.get_by_id(recipe_id=recipe_id)

        if recipe is None:
            return {'message': 'Recipe not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if recipe.is_publish == False and recipe.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return recipe.data(), HTTPStatus.OK 
        
    
#     def put(self, recipe_id):
#         data = request.get_json()
#         recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

#         if recipe is None:
#             return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
#         recipe.name = data['name']
#         recipe.description = data['description']
#         recipe.num_of_servings = data['num_of_servings']
#         recipe.cook_time = data['cook_time']
#         recipe.directions = data['directions']
#         return recipe.data, HTTPStatus.OK

#     def delete(self, recipe_id):
#         recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

#         if recipe is None:
#             return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND

#         recipe_list.remove(recipe)

#         return {}, HTTPStatus.NO_CONTENT


# class RecipePublishResource(Resource):
#     def put(self, recipe_id):
#         recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

#         if recipe is None:
#             return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
#         recipe.is_publish = True

#         return {}, HTTPStatus.NO_CONTENT
    
#     def delete(self, recipe_id):
#         recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

#         if recipe is None:
#             return {'message': 'recipe not found'}, HTTPStatus.NOT_FOUND
        
#         recipe.is_publish = False

#         return {}, HTTPStatus.NO_CONTENT
    
