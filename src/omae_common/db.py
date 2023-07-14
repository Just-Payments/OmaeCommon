import pymysql

from django.db import connections


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    "Return a row from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row != None:
        return dict(zip(columns, row))
    else:
        return None


def get_data_by_raw_query(sql, param=None, dbname="default"):
    with connections[dbname].cursor() as cursor:
        cursor.execute(sql, param)
        rows = dictfetchall(cursor=cursor)

    return rows


def get_one_by_raw_query(sql, param=None, dbname="default"):
    with connections[dbname].cursor() as cursor:
        cursor.execute(sql, param)
        row = dictfetchone(cursor=cursor)

    return row


def run_raw_query(sql, param=None, dbname="default") -> None:
    with connections[dbname].cursor() as cursor:
        cursor.execute(sql, param)


def get_data_from_mysql_db(sql: str, host: str, user: str, passwd: str,
                           db: str, charset: str = 'utf8mb4'):
    con = pymysql.connect(host=host, user=user, password=passwd,
                          db=db, charset=charset)
    cursor = con.cursor()
    cursor.execute(sql)
    rows = dictfetchall(cursor)
    con.close()
    return rows


def get_key_value_from_db(sql: str, dbconf: dict, key: str, value: str):
    rows = get_data_from_mysql_db(sql, dbconf["HOST"], dbconf["USER"],
                                  dbconf["PASSWORD"], dbconf["NAME"])

    kv = {}
    for data in rows:
        kv[data[key]] = data[value]

    return kv