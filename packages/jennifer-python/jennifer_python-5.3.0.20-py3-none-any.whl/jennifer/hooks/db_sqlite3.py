__hooking_module__ = 'sqlite3'


def connection_info(database, *args, **kwargs):
    return 'localhost', 0, database


def hook(sqlite3):
    from jennifer.wrap import db_api
    db_api.register_database(sqlite3.dbapi2, connection_info)
