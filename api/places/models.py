from libs.models import BaseModel


class Place(BaseModel):
    """
    Модель POI (пока это залы)
        owner_id - ссылка на владелеца
        lat, lng - долгота и широта
        enabled - флаг "место доступно на сайте"

        title - заголовок
        description - описание
        address - адрес
        ( данные поля, вероятно, логично заполнять только на языке владельца места )
    """

    class Meta:
        fields = ('owner_id', 'lat', 'lng', 'enabled')
        translations = ('title', 'description', 'address')
