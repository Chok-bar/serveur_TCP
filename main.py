import os
import socketserver


class ServerTCP(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        pieces = [b""]
        total = 0
        while b"\n" not in pieces[-1] and total < 10_000:
            pieces.append(self.request.recv(2000))
            total += len(pieces[-1])
        self.data = b"".join(pieces)
        print(f"Received from {self.client_address[0]}:")
        print(self.data.decode("utf-8"))

        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    SERVER_ADDRESS = os.getenv("TP_GAME_SERVER_ADDRESS")

    HOST, PORT = "localhost", 9999

    with socketserver.TCPServer((HOST, PORT), ServerTCP) as server:
        server.serve_forever()
