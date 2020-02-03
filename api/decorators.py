from flask import request, abort
from libs.http import HTTP_403_FORBIDDEN
from datetime import datetime


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


def user_is_subscriber(func):
    def wrapper(*args, **kwargs):
        u = request.user
        current_date = datetime.date(datetime.today())

        if u and u.subscribed_till and u.subscribed_till >= current_date:
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
