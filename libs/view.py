from flask import jsonify
from flask.views import MethodView
from libs.http import HTTP_200_OK


class View(MethodView):
    def make_response(self, resp):
        """
        Make api response from given data.
        """

        def serialize(obj):
            return obj.to_dict() if hasattr(obj, 'to_dict') else obj

        if type(resp) is int:
            # http code only
            return {}, resp

        elif type(resp) is dict:
            response_code = resp['_code'] if '_code' in resp else HTTP_200_OK

            d = {}
            for k in resp:
                if k != '_code':
                    item = resp[k]
                    if type(item) is list:
                        d[k] = []
                        for o in item:
                            d[k].append(serialize(o))
                    else:
                        d[k] = serialize(item)

            return jsonify(d), response_code
