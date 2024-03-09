import pickle
import socket
from _thread import start_new_thread

from Deck import Deck
from Hand import Hand

deck = Deck()

player_one = Hand()
player_two = Hand()
player_three = Hand()
player_four = Hand()

players = [player_one, player_two, player_three, player_four]

server = "192.168.0.103"
port = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as err:
    str(err)

s.listen(4)
print("Server started, waiting for connections...")

should_restart_game = False


def initial_deal():
    for hand in players:
        hand.add_card(deck.deal_card())


def is_round_end():
    for hand in players:
        if len(hand.cards) > 0:
            return False
    return True


def threaded_client(connection, player):
    global should_restart_game

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
                    reply = (players[1], players[2], players[3], is_round_end())
                elif player == 1:
                    reply = (players[2], players[3], players[0], is_round_end())
                elif player == 2:
                    reply = (players[3], players[0], players[1], is_round_end())
                else:
                    reply = (players[0], players[1], players[2], is_round_end())

                print(f"Received: {data}")
                print(f"Sending: {reply}")

            connection.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    connection.close()


current_player = 0
initial_deal()
while True:
    connection, address = s.accept()
    print(f"Connected to {address}")

    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1
