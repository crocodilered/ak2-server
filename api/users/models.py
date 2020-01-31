from libs.models import BaseModel


class User(BaseModel):
    """
    User Model for storing users related details
    """

    class Meta:
        fields = (
            'name',
            'email',
            'password',
            'authorized',
            'subscribed_till',
            'enabled',
            'admin'
        )
