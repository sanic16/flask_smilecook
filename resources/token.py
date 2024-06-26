from http import HTTPStatus
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from utils.common import check_password
from models.user import User
from models.token import TokenBlocklist
from datetime import datetime, timezone

class TokenResource(Resource):
    def post(self):
        json_data = request.get_json()
        email = json_data.get('email')
        password = json_data.get('password')
        user = User.get_by_email(email=email)

        if not user or not check_password(password, user.password):
            return {'message': 'email or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        if user.is_active is False:
            return {'message': 'The user account is not activated yet'}, HTTPStatus.FORBIDDEN
        
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)

        return {'access_token': access_token, 'refresh_token': refresh_token}, HTTPStatus.OK
    
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user, fresh=False)

        return {'access_token': access_token}, HTTPStatus.OK
    

class RevokeResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        type = get_jwt()['type']
        now = datetime.now(timezone.utc)
        TokenBlocklist(jti=jti, created_at=now, type=type).add()
        return {'message': 'Successfully logged out'}, HTTPStatus.OK     
    

class RevokeRefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        type = get_jwt()['type']
        now = datetime.now(timezone.utc)
        TokenBlocklist(jti=jti, created_at=now, type=type).add()
        return {'message': 'Successfully logged out'}, HTTPStatus.OK
    
