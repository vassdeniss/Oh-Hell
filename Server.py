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


def initial_deal():
    global trump
    
    for hand in players:
        hand.add_card(deck.deal_card())
    trump = deck.deal_card()


def is_round_end():
    global has_deck_reset

    for hand in players:
        if len(hand.cards) > 0:
            has_deck_reset = False
            return False
    return True


has_deck_reset = False
game_round = 2
trump = None


def threaded_client(connection, player):
    global game_round, trump
    global has_deck_reset

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
                cards = []
                if is_round_end():
                    if not has_deck_reset:
                        deck.reset()
                        has_deck_reset = True
                        trump = None
                    for _ in range(game_round):
                        cards.append(deck.deal_card())

                if sum(len(hand.cards) for hand in players) == game_round * 4 and trump is None:
                    trump = deck.deal_card()

                if player == 0:
                    reply = (players[1], players[2], players[3], cards, trump)
                elif player == 1:
                    reply = (players[2], players[3], players[0], cards, trump)
                elif player == 2:
                    reply = (players[3], players[0], players[1], cards, trump)
                else:
                    reply = (players[0], players[1], players[2], cards, trump)

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
