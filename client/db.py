import socket

class PyDBClient:

    def __init__(self):
        self.connection = None

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
        self.connection.sendall("PING".encode())

    def connect(self, host='127.0.0.1', port=9000):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_con:
            server_con.connect((host, port))
            self.connection = server_con
            # s.sendall(message.encode())
            # response = s.recv(1024)
            # return response.decode()
