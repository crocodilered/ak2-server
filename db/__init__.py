class Db:
    def __init__(self, conn, schema='public'):
        self.conn = conn
        self.schema = schema

    def save(self, o, **kwargs):
        if hasattr(o, 'get_db_manager'):
            db_manager = o.get_db_manager()
            return db_manager.save(self.conn, self.schema, o, **kwargs)

    def delete(self, o, **kwargs):
        if hasattr(o, 'get_db_manager'):
            db_manager = o.get_db_manager()
            return db_manager.delete(self.conn, self.schema, o, **kwargs)

    def get(self, t, **kwargs):
        if hasattr(t, 'get_db_manager'):
            db_manager = t.get_db_manager()
            return db_manager.get(self.conn, self.schema, **kwargs)

    def list(self, t, **kwargs):
        if hasattr(t, 'get_db_manager'):
            db_manager = t.get_db_manager()
            return db_manager.list(self.conn, self.schema, **kwargs)
