import json


class Action:

    def __init__(self, req):

        action_data = json.loads(req)

        self.query = action_data["query"]
        self.type = action_data["action"]
        self.payload = action_data["payload"]

    def __str__(self):

        act = [self.type]
        if self.payload:
            act.append(json.dumps(self.payload))
        if self.query:
            act.append(json.dumps(self.payload))

        return f"Action({', '.join(act)})"
