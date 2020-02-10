from flask import Blueprint, request, abort

from api import db
from api.shortcuts import db_get_or_404
from libs.views import View
from libs.http import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from .models import Place

from api.decorators import user_is_admin, user_logged_in


class PlacesListApi(View):
    @user_is_admin
    def get(self):
        """ List """
        return self.make_response({
            'places': db.list(Place)
        })

    @user_is_admin
    def post(self):
        """ Post new record to database """
        data = request.get_json().get('place')

        if data is None:
            abort(HTTP_400_BAD_REQUEST)

        place = Place(**data)
        place = db.save(place)

        if place is None:
            abort(HTTP_500_INTERNAL_SERVER_ERROR)

        response = {'place': place}

        return self.make_response(response)


class PlacesRetrieveApi(View):
    def get(self, place_id):
        place = db_get_or_404(Place, id=place_id)
        return self.make_response({'place': place})

    @user_logged_in
    def patch(self, place_id):
        data = request.get_json().get('place')

        if (
            data is None
            or (data.get('id') is not None and data['id'] != place_id)
        ):
            abort(HTTP_400_BAD_REQUEST)

        place = db_get_or_404(Place, id=place_id)

        if place.owner_id != request.user.id:
            abort(HTTP_403_FORBIDDEN)

        for attr in Place.Meta.fields:
            if data.get(attr) is not None:
                setattr(place, attr, data[attr])

        db.save(place)

        return self.make_response({'place': place})

    @user_is_admin
    def delete(self, place_id):
        db.delete(Place, id=place_id)
        return self.make_response(HTTP_204_NO_CONTENT)


# Add Rules for API Endpoints
places_blueprint = Blueprint('places', __name__)

places_blueprint.add_url_rule(
    '/',
    methods=['GET', 'POST'],
    view_func=PlacesListApi.as_view('places_list_view'),
)

places_blueprint.add_url_rule(
    '/<int:place_id>/',
    methods=['GET', 'PATCH', 'DELETE'],
    view_func=PlacesRetrieveApi.as_view('places_retrieve_view')
)
