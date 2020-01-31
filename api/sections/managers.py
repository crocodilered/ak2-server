from libs.managers import BaseManager
from .models import Section


class SectionManager(BaseManager):
    """
    DB manager for Section model.
    """

    class Meta:
        model = Section
        table = 'section'
