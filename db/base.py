class BaseDb:
    @staticmethod
    def list(conn, schema, **kwargs):
        raise Exception('Method must be implemented by child.')

    @staticmethod
    def get(conn, schema, **kwargs):
        raise Exception('Method must be implemented by child.')

    @staticmethod
    def save(conn, schema, o, **kwargs):
        raise Exception('Method must be implemented by child.')

    @staticmethod
    def delete(conn, schema, o, **kwargs):
        raise Exception('Method must be implemented by child.')
