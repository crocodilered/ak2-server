from libs.models import BaseModel


class Section(BaseModel):
    """
    Section item model.
        id - идентификатор
        parent_id - Ссылка на родителя
        title - заголовок раздела
        enabled - флаг "раздел доступен на сайте"
    """

    class Meta:
        fields = ('parent_id', 'enabled', 'order_key')
        translations = ('title', 'description')
