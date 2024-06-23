from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensions import db, jwt
from models.user import User
from models.token import TokenBlocklist 
from resources.recipe import RecipeListResource, RecipeResource 
from resources.user import UserListResource, UserResource, MeResource
from resources.token import TokenResource, RefreshResource, RevokeResource, RevokeRefreshResource 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app=app)
    register_resources(app=app)
    return app

def register_extensions(app):
    db.init_app(app=app)
    migrate = Migrate(app=app, db=db)
    jwt.init_app(app=app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

def register_resources(app):
    api = Api(app=app)
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    # api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')
    api.add_resource(RevokeRefreshResource, '/revoke_refresh')


app = create_app()

if __name__ == '__main__':    
    app.run()