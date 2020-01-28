from flask import Blueprint, request, abort

from api import db
from libs.view import View
from libs.http import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from models.section import Section

from api.decorators import user_is_admin


class SectionsListApi(View):
    @user_is_admin
    def get(self):
        """ List """
        return self.make_response({
            'sections': db.list(Section)
        })

    @user_is_admin
    def post(self):
        """ Post new record to database """
        params = request.get_json()
        response = HTTP_404_NOT_FOUND

        if 'section' in params:
            data = params.get('section')
            section = Section(**data)
            section = db.save(section)

            # Guard.
            if section is None:
                abort(HTTP_500_INTERNAL_SERVER_ERROR)

            response = {'section': section}

        return self.make_response(response)


class SectionsRetrieveApi(View):
    @user_is_admin
    def get(self, section_id):
        section = db.get(Section, id=section_id)
        resp = {'section': section} if section else HTTP_404_NOT_FOUND
        return self.make_response(resp)

    @user_is_admin
    def put(self, section_id):
        params = request.get_json()
        response = HTTP_404_NOT_FOUND

        if 'section' in params:
            data = params['section']
            section = Section(**data)
            db.save(section)
            response = {'section': section}

        return self.make_response(response)

    @user_is_admin
    def delete(self, section_id):
        db.delete(Section, id=section_id)
        return self.make_response(HTTP_204_NO_CONTENT)


class SectionsTreeApi(View):
    """ Tree view """
    def get(self):

        def _gen_siblings(sections, parent_id):
            r = []
            for section in sections:
                if section.parent_id == parent_id:
                    d = section.to_dict()
                    siblings = _gen_siblings(sections, section.id)
                    if siblings:
                        d['children'] = siblings
                    r.append(d)
            return r

        sections = db.list(Section, enabled=True)
        tree = _gen_siblings(sections, 0)

        return self.make_response({
            'tree': tree
        })


# Add Rules for API Endpoints
sections_blueprint = Blueprint('sections', __name__)

sections_blueprint.add_url_rule(
    '/',
    methods=['GET', 'POST'],
    view_func=SectionsListApi.as_view('sections_list_view'),
)

sections_blueprint.add_url_rule(
    '/<int:section_id>/',
    methods=['GET', 'PUT', 'DELETE'],
    view_func=SectionsRetrieveApi.as_view('sections_retrieve_view')
)

sections_blueprint.add_url_rule(
    '/_tree/',
    methods=['GET'],
    view_func=SectionsTreeApi.as_view('sections_tree_view'),
)
