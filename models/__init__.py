class BaseModel:
    def to_dict(self):
        raise Exception('Method must be implemented by child.')

    def to_row(self):
        raise Exception('Method must be implemented by child.')

    @staticmethod
    def from_row(self):
        raise Exception('Method must be implemented by child.')

    @staticmethod
    def get_db_manager():
        raise Exception('Method must be implemented by child.')
