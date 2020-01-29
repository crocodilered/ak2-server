from libs.db import DbManager
from api.users.models import User


class UserDb(DbManager):

    MODEL = User

    @staticmethod
    def get(conn, schema, *args, **kwargs):
        sql = f'''
            SELECT name, email, password, authorized, enabled, admin, id
            FROM {schema}.user
            WHERE 
        '''

        cursor = conn.cursor()

        if 'id' in kwargs:
            cursor.execute(sql + 'id = %s', (kwargs.get('id'),))

        elif 'email' in kwargs:
            cursor.execute(sql + 'email = %s', (kwargs.get('email'),))

        else:
            raise Exception('Bad params')

        row = cursor.fetchone()

        if row is not None:
            cursor.close()
            return User.from_row(row)

    @staticmethod
    def list(conn, schema, *args, **kwargs):
        sql = f'''
            SELECT name, email, password, authorized, enabled, admin, id
            FROM {schema}.user
            ORDER BY email 
        '''

        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()

        return [User.from_row(row) for row in rows]

    @staticmethod
    def save(conn, schema, o, **kwargs):
        cursor = conn.cursor()

        if o.id is None:
            sql = f'''
                INSERT INTO {schema}.user (name, email, password, authorized, enabled, admin)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            '''
            row = o.to_row()
            row.pop()

            try:
                cursor.execute(sql, row)
                o.id = cursor.fetchone()[0]
            except:
                conn.rollback()

        else:
            sql = f'''
                UPDATE {schema}.user SET
                    name = %s, 
                    email = %s,
                    password = %s, 
                    authorized = %s, 
                    enabled = %s,
                    admin = %s
                WHERE id = %s
            '''

            row = o.to_row()

            try:
                cursor.execute(sql, row)
            except:
                conn.rollback()

        cursor.close()
        conn.commit()

        return o
