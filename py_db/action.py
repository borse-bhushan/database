import json


class Action:

    def __init__(self, action, query=None, payload=None, auth=None):

        self.auth = auth
        self.query = query
        self.action = action
        self.payload = payload

    def __str__(self):

        act = [self.action]

        if self.auth:
            act.append(json.dumps(self.auth))

        if self.payload:
            act.append(json.dumps(self.payload))

        if self.query:
            act.append(json.dumps(self.query))

        return f"Action({', '.join(act)})"
