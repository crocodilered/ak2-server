from flask import Blueprint, request, abort

from api import db
from api.shortcuts import db_get_or_404
from api.decorators import user_is_admin, user_logged_in
from libs.views import View
from libs.http import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from .models import Video


class VideosListApi(View):
    def get(self):
        """ List """
        params = {
            'enabled': False
        }
        return self.make_response({
            'videos': db.list(Video, **params)
        })

    @user_is_admin
    def post(self):
        """ Post new record to database """
        data = request.get_json().get('video')

        if data is None or data.get('id') is not None:
            abort(HTTP_400_BAD_REQUEST)

        video = Video(**data)

        if db.save(video) is None:
            abort(HTTP_500_INTERNAL_SERVER_ERROR)

        response = {'video': video}

        return self.make_response(response)


class VideosRetrieveApi(View):
    @user_is_admin
    def get(self, video_id):
        video = db_get_or_404(Video, id=video_id)
        return self.make_response({'video': video})

    @user_is_admin
    def patch(self, video_id):
        data = request.get_json().get('video')

        if (
            data is None
            or (data.get('id') is not None and data['id'] != video_id)
        ):
            abort(HTTP_400_BAD_REQUEST)

        video = db_get_or_404(Video, id=video_id)

        # Fill model with data
        for attr in ('section_id', 'media_fp', 'enabled', 'order_key'):
            if data.get(attr) is not None:
                setattr(video, attr, data[attr])

        video.title.update(data.get('title'))
        video.description.update(data.get('description'))

        if db.save(video) is None:
            abort(HTTP_500_INTERNAL_SERVER_ERROR)

        return self.make_response({'video': video})

    @user_is_admin
    def delete(self, video_id):
        if db.delete(Video, id=video_id) is False:
            abort(HTTP_500_INTERNAL_SERVER_ERROR)

        return self.make_response(HTTP_204_NO_CONTENT)


class VideosShowApi(View):
    """ Show view """

    @user_logged_in
    def get(self):
        return self.make_response({
            'show': None
        })


# Add Rules for API Endpoints
videos_blueprint = Blueprint('videos', __name__)

videos_blueprint.add_url_rule(
    '/',
    methods=['GET', 'POST'],
    view_func=VideosListApi.as_view('videos_list_view'),
)

videos_blueprint.add_url_rule(
    '/<int:video_id>/',
    methods=['GET', 'PATCH', 'DELETE'],
    view_func=VideosRetrieveApi.as_view('videos_retrieve_view')
)

videos_blueprint.add_url_rule(
    '/_show/',
    methods=['GET'],
    view_func=VideosShowApi.as_view('videos_show_view'),
)
