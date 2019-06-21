from django.db import connection
from collections import namedtuple


def raw_sql(sql, params=[]):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        desc = cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in cursor.fetchall()]