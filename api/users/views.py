from flask import Blueprint, request, abort

from api import db
from api.shortcuts import db_get_or_404
from libs.view import View
from libs.http import HTTP_400_BAD_REQUEST
from models.user import User

from api.decorators import user_is_admin, user_is_admin_or_self


class UsersListApi(View):
    @user_is_admin
    def get(self):
        """ List """
        return self.make_response({
            'users': db.list(User)
        })


class UsersRetrieveApi(View):
    """
    User model Resource.
    """
    @user_is_admin_or_self
    def get(self, user_id):
        user = db_get_or_404(User, id=user_id)
        return self.make_response({'user': user})

    @user_is_admin_or_self
    def patch(self, user_id):
        params = request.get_json()
        data = params.get('user')

        if (
            data is None
            or (data.get('id') is not None and data['id'] != user_id)
            or data.get('email')
            or data.get('password')
        ):
            abort(HTTP_400_BAD_REQUEST)

        user = db_get_or_404(User, id=user_id)

        for attr in User.FIELDS:
            if data.get(attr) is not None:
                setattr(user, attr, data[attr])

        db.save(user)

        return self.make_response({'user': user})


# Add Rules for API Endpoints
users_blueprint = Blueprint('users', __name__)

users_blueprint.add_url_rule(
    '/',
    methods=['GET'],
    view_func=UsersListApi.as_view('users_list_view'),
)

users_blueprint.add_url_rule(
    '/<int:user_id>/',
    methods=['GET', 'PATCH'],
    view_func=UsersRetrieveApi.as_view('users_retrieve_view')
)
