from libs.models import BaseModel


class Video(BaseModel):
    """
    Video model.
        id - идентификатор
        title - заголовок видео, i18n
        media_fp - путь к файлу с видео
        enabled - флаг "видео доступно на сайте"
        order_key - ключ сортировки
    """

    class Meta:
        fields = ('section_id', 'media_fp', 'enabled', 'order_key')
        translations = ('title', 'description')
