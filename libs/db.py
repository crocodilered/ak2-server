from api.users.managers import UserManager
from api.users.models import User

from api.sections.managers import SectionManager
from api.sections.models import Section

from api.videos.managers import VideoManager
from api.videos.models import Video


def get_manager(model):

    t = model

    if type(model) != type:
        t = type(model)

    if t == Section:
        return SectionManager

    if t == User:
        return UserManager

    if t == Video:
        return VideoManager


class Db(object):
    """
    Database singleton's class.
    """
    def __init__(self, conn, schema='public'):
        self.conn = conn
        self.schema = schema

    def save(self, model_obj, **kwargs):
        manager = get_manager(model_obj)
        return manager.save(self.conn, self.schema, model_obj, **kwargs)

    def delete(self, model_cls, **kwargs):
        manager = get_manager(model_cls)
        return manager.delete(self.conn, self.schema, **kwargs)

    def get(self, model_cls, **kwargs):
        manager = get_manager(model_cls)
        return manager.get(self.conn, self.schema, **kwargs)

    def list(self, model_cls, **kwargs):
        manager = get_manager(model_cls)
        return manager.list(self.conn, self.schema, **kwargs)

    def run(self, model_cls, command, **kwargs):
        """ Run custom manager method. """
        manager = get_manager(model_cls)
        manager_attr = getattr(manager, command)
        return manager_attr(self.conn, self.schema, **kwargs)
