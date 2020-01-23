from flask import Blueprint, request

from libs.http import *
from api import bcrypt, db
from libs.view import View
from models.user import User

from . import encode_auth_token


class RegisterAPI(View):
    """
    User Registration Resource.
    """
    @staticmethod
    def _check_email_format(email):
        """ Check email format. """
        return type(email) == str and '@' in email and '.' in email

    def post(self):
        params = request.get_json()

        if not RegisterAPI._check_email_format(params.get('email')):
            return self.make_response(HTTP_400_BAD_REQUEST)

        # Check if users already exists
        if db.get(User, email=params.get('email')) is not None:
            return self.make_response({'message': 'user-already-exists'})

        # Can create new users now
        user = User(
            params.get('name'),
            params.get('email'),
            '',
            True,
            True,
            False
        )
        user.set_password(params.get('password'))
        db.save(user)

        # Generate the auth.py token
        auth_token = encode_auth_token(user.id)

        return self.make_response({
            'auth_token': auth_token.decode(),
            'user': user
        })


class LoginAPI(View):
    """
    User Login Resource.
    """
    def post(self):
        """ Login users. """
        params = request.get_json()

        # Try to get users with given email.
        # No need to check email format here.
        user = db.get(User, email=params.get('email'))

        if not user:
            return self.make_response({'message': 'user-doesnt-exist'})

        if not user.enabled:
            return self.make_response({'message': 'user-isnt-enabled.'})

        if not bcrypt.check_password_hash(user.password, params.get('password')):
            return self.make_response({'message': 'password-mismatched'})

        # All guards passed.

        auth_token = encode_auth_token(user.id)

        user.authorized = True
        db.save(user)

        return self.make_response({
            'auth_token': auth_token.decode(),
            'user': user
        })


class LogoutAPI(View):
    """
    Logout resource.
    """
    def post(self):
        resp = self.PERMISSION_DENIED_RESP  # default value

        if request.user is not None:
            request.user.authorized = False
            db.save(request.user)
            resp = HTTP_204_NO_CONTENT

        return self.make_response(resp)


class StatusAPI(View):
    """
    Current user props resource.
    """
    def get(self):
        if request.user is None:
            return self.make_response(self.PERMISSION_DENIED_RESP)

        return self.make_response({'user': request.user})


class PasswordApi(View):
    """
    Set new user password resource.
    """
    def post(self):
        params = request.get_json()
        current_pw = params.get('current')
        candidate_pw = params.get('candidate')

        if request.user is None:
            return self.make_response(self.PERMISSION_DENIED_RESP)

        # check current password
        if not bcrypt.check_password_hash(request.user.password, current_pw):
            return self.make_response({'message': 'password-mismatched'})

        request.user.set_password(candidate_pw)
        db.save(request.user)

        return self.make_response(HTTP_204_NO_CONTENT)


# Add Rules for API Endpoints
auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.add_url_rule(
    '/register/',
    methods=['POST'],
    view_func=RegisterAPI.as_view('register_api')
)
auth_blueprint.add_url_rule(
    '/login/',
    methods=['POST'],
    view_func=LoginAPI.as_view('login_api')
)
auth_blueprint.add_url_rule(
    '/status/',
    methods=['GET'],
    view_func=StatusAPI.as_view('status_api')
)
auth_blueprint.add_url_rule(
    '/logout/',
    methods=['POST'],
    view_func=LogoutAPI.as_view('logout_api')
)
auth_blueprint.add_url_rule(
    '/password/',
    methods=['POST'],
    view_func=PasswordApi.as_view('password_api')
)
