from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def hash_password(password):
    return pbkdf2_sha256.hash(password)

def check_password(password, hashed):
    return pbkdf2_sha256.verify(password, hashed)

def generate_confirmation_token(*args, salt=None):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
    return serializer.dumps(args, salt=salt)

def verify_token(token, max_age=(30*60), salt=None):
    serializer = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))

    try:
        keys = serializer.loads(
            token,
            salt=salt,
            max_age=max_age
        )
    except:
        return False
    
    return keys
