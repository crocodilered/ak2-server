from flask import request
import jwt
import datetime
from api import app, bcrypt, db


def encode_password(password):
    """ Кодировка пароля """
    password = bcrypt.generate_password_hash(
        password,
        app.config.get('BCRYPT_LOG_ROUNDS')
    )
    return password.decode()


def encode_auth_token(user_id):
    """ Кодировка токена. """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365*100),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        print(e)


def decode_auth_token(auth_token):
    """ Раскодировка токена. """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub'], None
    except jwt.ExpiredSignatureError:
        return None, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return None, 'Invalid token. Please log in again.'


@app.before_request
def apply_user_to_request():

    if request.method == 'OPTIONS':
        return

    # Default value
    request.user = None

    from models.user import User
    from api.auth import decode_auth_token

    auth_header = request.headers.get('Authorization')

    if auth_header:
        auth_token = auth_header.split(' ')[1]
        payload, err_message = decode_auth_token(auth_token)
        if payload is not None:
            user = db.get(User, id=payload)
            if user and user.authorized:
                request.user = user
