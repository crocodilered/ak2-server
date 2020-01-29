from flask import abort

from api import db
from libs.http import HTTP_404_NOT_FOUND


def db_get_or_404(cls, **kwargs):
    obj = db.get(cls, **kwargs)

    if obj is None:
        abort(HTTP_404_NOT_FOUND)

    return obj
