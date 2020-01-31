from psycopg2.extras import execute_values


class BaseManager(object):
    """
    Abstract model database manager
    """

    class Meta:
        model = None
        table = None

    @classmethod
    def __model_has_translations(cls):
        return (
            hasattr(cls.Meta.model.Meta, 'translations')
            and len(cls.Meta.model.Meta.translations) > 0
        )

    @classmethod
    def __load_translations(cls, conn, schema, **kwargs):
        """
        Get translations for raw(s) identified with id or raws (list of raws).
        :param kwargs
            id
            raws
        :returns dict of translations (lookup).
        """
        result = {}

        if cls.__model_has_translations():
            cur = conn.cursor()
            ids = None

            if type(kwargs.get('id')) == int:
                ids = (kwargs.get('id'),)

            elif type(kwargs.get('raws')) == list:
                raws = kwargs.get('raws')
                ids = tuple(i[-1] for i in raws)

            if ids:
                cur.execute(
                    f'''
                        SELECT {cls.Meta.table}_id, code, lang, value
                        FROM {schema}.i18n
                        WHERE {cls.Meta.table}_id IN %s
                    ''',
                    (ids,)
                )

                translations = cur.fetchall()

                # build lookup
                result = {i: [] for i in ids}

                # populate lookup
                for t in translations:
                    result[t[0]].append(t[1:])

            cur.close()

        return result

    @classmethod
    def get(cls, conn, schema, **kwargs):
        """ Get record by id """

        record_id = kwargs.get('id')
        cur = conn.cursor()
        result = None

        cur.execute(
            f'''
                SELECT {','.join(cls.Meta.model.Meta.fields)}, id
                FROM {schema}.{cls.Meta.table}
                WHERE id = %s
            ''',
            (record_id,)
        )

        raw = cur.fetchone()

        if raw:
            translations = cls.__load_translations(conn, schema, id=record_id)
            result = cls.Meta.model.from_raw(
                raw,
                translations.get(record_id)
            )

        cur.close()

        return result

    @classmethod
    def delete(cls, conn, schema, **kwargs):
        """ Delete record by id """

        record_id = kwargs.get('id')
        cur = conn.cursor()
        result = False

        try:
            # Translations will be deleted cascade
            sql = f'DELETE FROM {schema}.{cls.Meta.table} WHERE id = %s'
            cur.execute(sql, (record_id,))
            conn.commit()
            result = True
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            cur.close()

        return result

    @classmethod
    def list(cls, conn, schema, **kwargs):
        result = []
        cur = conn.cursor()
        conditions_sql = ''
        conditions_data = []

        if 'enabled' in kwargs:
            conditions_sql += ' AND enabled = %s'
            conditions_data.append(kwargs['enabled'])

        sql = f'''
            SELECT {','.join(cls.Meta.model.Meta.fields)}, id
            FROM {schema}.{cls.Meta.table}
            WHERE 1 = 1 {conditions_sql}
        '''

        if 'order_key' in cls.Meta.model.Meta.fields:
            sql += ' ORDER BY order_key'

        # Get objects
        cur.execute(sql, conditions_data)
        raws = cur.fetchall()
        cur.close()

        # Get translates
        if raws:
            translations = cls.__load_translations(conn, schema, raws=raws)
            for i in raws:
                obj = cls.Meta.model.from_raw(i, translations.get(i[-1]))
                result.append(obj)

        return result

    @classmethod
    def save(cls, conn, schema, model, **kwargs):

        def insert_model():
            fields = list(cls.Meta.model.Meta.fields)

            # Remove order_key from fields list: they have default value.
            if 'order_key' in fields:
                fields.remove('order_key')

            fields_names = ','.join(fields)
            fields_values = ','.join(['%s' for i in fields])

            sql = f'''
                INSERT INTO {schema}.{cls.Meta.table} ( {fields_names} ) 
                VALUES ( {fields_values} )
                RETURNING id
            '''
            cur.execute(sql, raw[:-2])  # Remove order_key and id
            model.id = cur.fetchone()[0]

        def update_model():
            fields = ','.join([f'{i} = %s' for i in cls.Meta.model.Meta.fields])

            sql = f'''
                UPDATE {schema}.{cls.Meta.table} SET {fields}
                WHERE id = %s
            '''
            cur.execute(sql, raw)

        def insert_translations():
            sql = f'DELETE FROM {schema}.i18n WHERE {cls.Meta.table}_id = %s'
            cur.execute(sql, (model.id,))

            translations = model.get_all_translations()

            execute_values(
                cur,
                f'INSERT INTO {schema}.i18n ({cls.Meta.table}_id, lang, code, value) VALUES %s',
                translations
            )

        if model is None or type(model) != cls.Meta.model:
            return None

        raw = model.to_raw()
        cur = conn.cursor()
        result = None

        try:
            insert_model() if model.id is None else update_model()
            if cls.__model_has_translations():
                insert_translations()
            conn.commit()
            result = model
        except Exception as ex:
            conn.rollback()
            raise ex
        finally:
            cur.close()

        return result
