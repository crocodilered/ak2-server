from libs.models import BaseModel


class Section(BaseModel):
    """
    Section item model.
        parent_id - Ссылка на родителя
        enabled - флаг "раздел доступен на сайте"
        order_key - ключ сортировки

        title - заголовок раздела
        description - описание
    """

    class Meta:
        fields = (
            'parent_id',
            'enabled',
            'order_key'
        )
        translations = (
            'title',
            'description'
        )
