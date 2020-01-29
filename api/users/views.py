from flask import Blueprint, request

from api import db
from libs.view import View
from libs.http import HTTP_404_NOT_FOUND
from models.user import User

from api.decorators import user_is_admin, user_is_admin_or_self


class UserIndexApi(View):
    @user_is_admin
    def get(self):
        """ List """
        return self.make_response({
            'users': db.list(User)
        })


class UserDetailsApi(View):
    """
    User model Resource.
    """
    @user_is_admin_or_self
    def get(self, user_id):
        user = db.get(User, id=user_id)
        resp = {'user': user} if user else HTTP_404_NOT_FOUND
        return self.make_response(resp)

    @user_is_admin_or_self
    def put(self, user_id):
        params = request.get_json()
        user_data = params['user']

        user = db.get(User, id=user_id)

        if user_data.get('name') is not None:
            user.name = user_data['name']

        if user_data.get('email') is not None:
            user.email = user_data['email']

        if user_data.get('password') is not None:
            user.set_password(user_data['password'])

        db.save(user)

        return self.make_response({'user': user})


# Define the API resources
users_list_view = UserIndexApi.as_view('users_index_view')
users_details_view = UserDetailsApi.as_view('users_details_view')

# Add Rules for API Endpoints
users_blueprint = Blueprint('users', __name__)

users_blueprint.add_url_rule(
    '/',
    methods=['GET'],
    view_func=users_list_view,
)

users_blueprint.add_url_rule(
    '/<int:user_id>/',
    methods=['GET', 'PUT'],
    view_func=users_details_view
)
