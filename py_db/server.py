import socket
import threading

from .log import log_msg, logging

class TCPDBServer:
    def __init__(self, host='127.0.0.1', port=9000):
        self.host = host
        self.port = port

    def handle_client(self, conn, addr):
        log_msg(logging.DEBUG, f"[CONNECTED] {addr}")

        with conn:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    response = f"Echo from server: {data.decode()}"
                    conn.sendall(response.encode())
                except Exception as e:
                    print(f"[ERROR] {addr}: {e}")
                    break

        log_msg(logging.DEBUG, f"[DISCONNECTED] {addr}")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            log_msg(logging.DEBUG, f"[LISTENING] Server running on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                thread.start()

