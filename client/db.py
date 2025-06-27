import socket


class PyDBClient:

    def __init__(self, host="127.0.0.1", port=9000):
        self.connection = None

        self.host = host
        self.port = port

    def create(self, data, many=False):
        pass

    def find(self, query):
        pass

    def find_many(self, query):
        pass

    def update(self, query):
        pass

    def delete(self, query):
        pass

    def ping(self):
        response = self.connection.sendall("PING".encode())
        return response.decode()

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_con:
            server_con.connect((self.host, self.port))
            self.connection = server_con
