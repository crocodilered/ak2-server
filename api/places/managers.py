from libs.managers import BaseManager
from .models import Place


class PlaceManager(BaseManager):
    """
    DB manager for Place model.
    """

    class Meta:
        model = Place
        table = 'place'
