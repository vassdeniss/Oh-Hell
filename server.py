import pickle
import socket
from _thread import start_new_thread

from Hand import Hand

player_one = Hand()
player_two = Hand()
player_three = Hand()
player_four = Hand()

players = [player_one, player_two, player_three, player_four]

server = "192.168.0.30"
port = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as err:
    str(err)

s.listen(4)
print("Server started, waiting for connections...")


def threaded_client(connection, player):
    connection.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(connection.recv(2048))
            players[player] = data

            if not data:
                print("Disconneccted")
                break
            else:
                if player == 0:
                    reply = (players[1], players[2], players[3])
                elif player == 1:
                    reply = (players[2], players[3], players[0])
                elif player == 2:
                    reply = (players[3], players[0], players[1])
                else:
                    reply = (players[0], players[1], players[2])

                print(f"Received: {data}")
                print(f"Sending: {reply}")

            connection.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    connection.close()


current_player = 0
while True:
    connection, address = s.accept()
    print(f"Connected to {address}")

    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1
