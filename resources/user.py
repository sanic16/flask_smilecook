from flask import request, url_for
from flask_restful import Resource
from http import HTTPStatus
from utils.common import hash_password, generate_confirmation_token, verify_token
from utils.email import send_email
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        if User.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        password = hash_password(non_hash_password)

        user = User()
        user.username = username
        user.email = email
        user.password = password
        user.save()

        token = generate_confirmation_token(user.email, salt='activate')
        subject = 'Please confirm your registration'
        link = url_for('useractivateresource', token=token, _external=True)
        body = f'Your confirmation link is: {link}'
        recipient = user.email

        send_email(subject=subject, body=body, recipient=recipient)        

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return data, HTTPStatus.CREATED
    
class UserActivateResource(Resource):
    def get(self, token):
        email = verify_token(token, salt='activate')
        print(email[0])
        print(type(email[0]))
        if email is False:
            return {'message': 'Invalid token'}, HTTPStatus.BAD_REQUEST
        
        user = User.get_by_email(email=email[0])

        if not user:
            return {
                'message': 'User not found'
            }, HTTPStatus.NOT_FOUND
        
        if user.is_active is True:
            return {'message': 'The user account is already activated'}, HTTPStatus.BAD_REQUEST
        
        user.is_active = True

        user.save()

        return {}, HTTPStatus.NO_CONTENT
            

class UserResource(Resource):
    @jwt_required(optional=True)
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        else:
            data = {
                'id': user.id,
                'username': user.username
            }
        
        return data, HTTPStatus.OK

class MeResource(Resource):
    @jwt_required(optional=False)
    def get(self):
        user = User.get_by_id(user_id=get_jwt_identity())

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return data, HTTPStatus.OK