import json


class Action:

    def __init__(self, action, query=None, payload=None, auth=None, table=None):

        self.query = query
        self.table = table
        self.action = action
        self.payload = payload
        self.auth = auth or {}
        self.user_db_conf = {}

    def __str__(self):

        act = [self.action]


        if self.table:
            act.append(self.table)

        if self.payload:
            act.append(json.dumps(self.payload))

        if self.query:
            act.append(json.dumps(self.query))

        if self.auth:
            act.append(json.dumps(self.auth))

        return f"Action({', '.join(act)})"
