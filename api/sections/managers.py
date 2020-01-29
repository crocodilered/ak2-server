"""
DB manager for Section model.
"""

from libs.db import DbManager
from api.sections.models import Section


class SectionDbManager(DbManager):

    MODEL = Section

    @staticmethod
    def get(conn, schema, *args, **kwargs):
        sql = f'''
            SELECT parent_id, title, enabled, order_key, id
            FROM {schema}.section
            WHERE 
        '''

        cursor = conn.cursor()

        if 'id' in kwargs:
            cursor.execute(sql + 'id = %s', (kwargs.get('id'),))

        else:
            raise Exception('Bad params')

        row = cursor.fetchone()

        if row is not None:
            cursor.close()
            return Section.from_row(row)

    @staticmethod
    def delete(conn, schema, *args, **kwargs):
        result = False

        sql = f'''
            DELETE FROM {schema}.section
            WHERE 
        '''

        cursor = conn.cursor()

        if 'id' in kwargs:
            try:
                cursor.execute(sql + 'id = %s', (kwargs.get('id'),))
                result = True
            except:
                conn.rollback()

        cursor.close()

        return result

    @staticmethod
    def list(conn, schema, *args, **kwargs):
        conds_sql = ''
        conds_params = []

        if 'enabled' in kwargs:
            conds_sql += ' AND enabled = %s'
            conds_params.append(kwargs['enabled'])

        sql = f'''
            SELECT parent_id, title, enabled, order_key, id
            FROM {schema}.section
            WHERE 1 = 1 {conds_sql}
            ORDER BY order_key 
        '''

        cursor = conn.cursor()
        cursor.execute(sql, conds_params)
        rows = cursor.fetchall()
        cursor.close()

        return [Section.from_row(row) for row in rows]

    @staticmethod
    def save(conn, schema, o, **kwargs):
        cursor = conn.cursor()

        if o.id is None:
            sql = f'''
                INSERT INTO {schema}.section (
                    parent_id,
                    title,
                    enabled,
                    order_key
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    ( SELECT ROUND(extract(epoch from now())) )
                )
                RETURNING id
            '''

            try:
                row = o.to_row()
                cursor.execute(sql, row[:-2])  # Remove order_key and id
                o.id = cursor.fetchone()[0]
            except Exception as e:
                conn.rollback()
                return None

        else:
            sql = f'''
                UPDATE {schema}.section SET
                    parent_id = %s, 
                    title = %s,
                    enabled = %s,
                    order_key = %s
                WHERE id = %s
            '''

            row = o.to_row()

            try:
                cursor.execute(sql, row)
            except:
                conn.rollback()
                return None

        cursor.close()
        conn.commit()

        return o
