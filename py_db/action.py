import json


class Action:

    def __init__(self, req):

        action_data = json.loads(req)

        self.query = action_data["query"]
        self.type = action_data["action"]
        self.payload = action_data["payload"]
