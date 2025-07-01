from .auth import authentication


class ActionEnum:
    PING = "PING"

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    SELECT = "SELECT"

    CREATE_DATABASE = "CREATE_DATABASE"

    ERROR = "ERROR"

    LOGIN = authentication.add_exclude_action("LOGIN")
