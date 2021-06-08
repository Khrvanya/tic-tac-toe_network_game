import socket
import pickle


class Network:
    def __init__(self, server, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (server, port)
        self.player_conn = self.connect()

    def get_player_conn(self) -> int:
        return self.player_conn

    def connect(self):
        try:
            self.client.connect(self.addr)
            return int(self.client.recv(4096).decode())
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(str(data)))
            return pickle.loads(self.client.recv(4096))
        except socket.error as error:
            print(error)
