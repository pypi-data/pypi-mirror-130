__hooking_module__ = 'MySQLdb'


def safe(properties, idx, default=None):
    try:
        return properties[idx]
    except IndexError:
        return default


def connection_info(*args, **kwargs):
    host = safe(args, 0) or kwargs.get('host')
    port = safe(args, 6) or kwargs.get('port') or 3306
    database = safe(args, 4) or kwargs.get('database') or kwargs.get('db')

    return host, port, database


def hook(my_sql_db):
    from jennifer.wrap import db_api
    db_api.register_database(my_sql_db, connection_info)
