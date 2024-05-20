import socket
import pickle
from constants import LOCAL_IP


class Network:
    def __init__(self):
        self.client = self.create_socket()
        self.server = LOCAL_IP
        self.port = 3000
        self.address = (self.server, self.port)
        self.player = self.connect()

    def create_socket(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        return client

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048).decode()
        except:
            self.client.close()
            self.client = self.create_socket()
            return -1

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4048))
        except socket.error as err:
            print(err)

    def get_player(self):
        return self.player
