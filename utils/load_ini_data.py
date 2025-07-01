from py_db.storage import Storage


def load_ini_data_in_database(database_conf: list):

    storage_engine = Storage()
    for db_conf in database_conf:
        storage_engine.create_database(db_conf)
