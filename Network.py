import socket
import pickle
from constants import LOCAL_IP


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = LOCAL_IP
        self.port = 3000
        self.address = (self.server, self.port)
        self.player = self.connect()

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4048))
        except socket.error as err:
            print(err)

    def get_player(self):
        return self.player
