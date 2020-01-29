from .base import BaseModel
from api.auth import encode_password


class User(BaseModel):
    """
    User Model for storing users related details
    """

    FIELDS = ('name', 'email', 'password', 'authorized', 'enabled', 'admin', 'id')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name') or ''
        self.email = kwargs.get('email') or ''
        self.password = kwargs.get('password') or ''
        self.authorized = kwargs.get('authorized') or False
        self.enabled = kwargs.get('enabled') or False
        self.admin = kwargs.get('admin') or False

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    @staticmethod
    def from_row(row):
        """ Конструктор объекта на основе данных, прибывших их БД """
        user = None

        if type(row) is tuple and len(row) == 7:
            user = User(
                id=row[6],
                name=row[0],
                email=row[1],
                password=row[2],
                authorized=row[3],
                enabled=row[4],
                admin=row[5]
            )

        return user

    def to_row(self):
        return self.name, self.email, self.password, self.authorized, self.enabled, self.admin, self.id,

    @staticmethod
    def get_db_manager():
        from db.user import UserDb
        return UserDb
