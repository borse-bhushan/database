import socketserver


class DBRequestHandler(socketserver.ThreadingTCPServer):
    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            response = f"Echo from server: {data.decode()}"
            self.request.sendall(response.encode())


if __name__ == "__main__":
    with socketserver.ThreadingTCPServer(
        ("127.0.0.1", 9000), DBRequestHandler
    ) as server:
        print("TCP Server running on 127.0.0.1:9000")
        server.serve_forever()
