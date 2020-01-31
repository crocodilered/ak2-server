from libs.managers import BaseManager
from api.users.models import User


class UserManager(BaseManager):

    class Meta:
        model = User
        table = 'user'

    @staticmethod
    def get_by_email(conn, schema, **kwargs):
        """ Get record by email """

        meta_table = UserManager.Meta.table
        meta_model = UserManager.Meta.model
        meta_fields = meta_model.Meta.fields

        email = kwargs.get('email')
        result = None

        with conn.cursor() as cur:
            cur.execute(
                f'''
                    SELECT {','.join(meta_fields)}, id
                    FROM {schema}.{meta_table}
                    WHERE email = %s
                ''',
                (email,)
            )

            raw = cur.fetchone()

            if raw:
                result = meta_model.from_raw(raw)

        return result
