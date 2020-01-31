from libs.managers import BaseManager
from .models import Video


class VideoManager(BaseManager):
    """
    DB manager for Video model.
    """

    class Meta:
        model = Video
        table = 'video'
