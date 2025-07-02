import json


class Response:
    def __init__(self, act_type, resp_payload):

        self.act_type = act_type
        self.resp_payload = resp_payload

    def generate(self):

        return json.dumps({"action_type": self.act_type, "payload": self.resp_payload})
