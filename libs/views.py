from flask import jsonify, request
from flask.views import MethodView
from api import app
from libs.http import HTTP_200_OK


class View(MethodView):
    @property
    def lang(self):
        app_langs = app.config.get('LANGUAGES')

        for client_lang in request.accept_languages:
            if client_lang[0] == '*':
                return None
            else:
                for app_lang in app_langs:
                    prefix = f'{app_lang}-'
                    if app_lang == client_lang[0] or prefix == client_lang[0][:3]:
                        return app_lang

        return app_langs[0]

    def _detect_lang(self):
        """ Detect client's lang. """
        # Detect if accept all the languages

    def make_response(self, resp):
        """ Make api response from given data. """

        def serialize(obj):
            return obj.to_dict(self.lang) if hasattr(obj, 'to_dict') else obj

        if type(resp) is int:
            # http code only
            return {}, resp

        elif type(resp) is dict:
            response_code = resp['_code'] if '_code' in resp else HTTP_200_OK

            response_data = {}
            for k in resp:
                if k != '_code':
                    item = resp[k]
                    if type(item) is list:
                        response_data[k] = []
                        for o in item:
                            response_data[k].append(serialize(o))
                    else:
                        response_data[k] = serialize(item)

            return jsonify(response_data), response_code
