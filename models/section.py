from . import BaseModel


class Section(BaseModel):
    """
    Section item model.
        id - идентификатор
        parent_id - Ссылка на родителя
        title - заголовок раздела
        enabled - флаг "раздел доступен на сайте"
    """

    FIELDS = ('parent_id', 'title', 'enabled', 'order_key', 'id')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.parent_id = kwargs.get('parent_id') or 0
        self.title = kwargs.get('title') or ''
        self.enabled = kwargs.get('enabled') or False
        self.order_key = kwargs.get('order_key')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'parent_id': self.parent_id,
            'enabled': self.enabled,
            'order_key': self.order_key
        }

    @staticmethod
    def from_row(row):
        """ Конструктор объекта на основе данных, прибывших их БД """
        result = None

        if type(row) is tuple and len(row) == 5:
            result = Section(
                id=row[4],
                parent_id=row[0],
                title=row[1],
                enabled=row[2],
                order_key=row[3],
            )

        return result

    def to_row(self):
        return self.parent_id, self.title, self.enabled, self.order_key, self.id,

    @staticmethod
    def get_db_manager():
        from db.section import SectionDb
        return SectionDb
