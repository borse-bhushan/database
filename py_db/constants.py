from .auth import authentication


class ActionEnum:
    PING = "PING"

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SELECT = "SELECT"

    CREATE_TABLE = "CREATE_TABLE"
    CREATE_DATABASE = "CREATE_DATABASE"

    DROP_TABLE = "DROP_TABLE"
    # DROP_DATABASE = "DROP_DATABASE"

    ERROR = "ERROR"

    LOGIN = authentication.add_exclude_action("LOGIN")
