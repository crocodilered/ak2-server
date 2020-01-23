class User:
    """
    User Model for storing users related details
    """
    id = None           # идентификатор
    name = None         # имя
    email = None        # эл. почта
    password = None     # пароль (шифрованный)
    authorized = None   # флаг "пользователь в системе"
    enabled = None      # флаг "пользователь заблокирован"
    admin = None        # флаг "пользователь является админом"

    FIELDS = ('name', 'email', 'password', 'authorized', 'enabled', 'admin', 'id')

    def __init__(self, name, email, password, authorized, enabled=True, admin=False):
        self.id = None
        self.name = name
        self.email = email
        self.password = password
        self.authorized = authorized
        self.enabled = enabled
        self.admin = admin

    def set_password(self, password):
        from api.auth import encode_password
        self.password = encode_password(password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    @staticmethod
    def from_row(raw):
        """ Конструктор объекта на основе данных, прибывших их БД """
        user = None

        if type(raw) is tuple and len(raw) == 7:
            user = User(raw[0], raw[1], raw[2], raw[3], raw[4], raw[5])
            user.id = raw[6]

        return user

    def to_row(self):
        return [self.name, self.email, self.password, self.authorized, self.enabled, self.admin, self.id]

    @staticmethod
    def get_db_manager():
        from db.user import UserDb
        return UserDb
