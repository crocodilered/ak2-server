from flask import request, abort
from libs.http import HTTP_403_FORBIDDEN


def user_logged_in(func):
    def wrapper(*args, **kwargs):
        u = request.user
        if u:
            return func(*args, **kwargs)
        else:
            abort(HTTP_403_FORBIDDEN)

    return wrapper


def user_is_admin(func):
    def wrapper(*args, **kwargs):
        u = request.user
        if u and u.admin:
            return func(*args, **kwargs)
        else:
            abort(HTTP_403_FORBIDDEN)

    return wrapper


def user_is_admin_or_self(func):
    def wrapper(*args, **kwargs):
        u = request.user
        if u and (
            u.admin or
            u.id == kwargs['user_id']
        ):
            return func(*args, **kwargs)
        else:
            abort(HTTP_403_FORBIDDEN)

    return wrapper
