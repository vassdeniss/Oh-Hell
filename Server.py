import pickle
import random
import socket
from collections import deque
from _thread import start_new_thread
from constants import LOCAL_IP, PORT
from Deck import Deck
from Hand import Hand

deck = Deck()

player_one = Hand(0)
player_two = Hand(1)
player_three = Hand(2)
player_four = Hand(3)

history = deque()

players = [player_one, player_two, player_three, player_four]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((LOCAL_IP, PORT))
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


def has_all_bid():
    return all(player.bid != -1 for player in players)


def rotate_players():
    global dealer
    dealer = (dealer + 1) % 4


def get_total_takes():
    return sum(player.taken_hands for player in players)


has_deck_reset = False
game_round = 1
trump = None
has_bidding_phase_finished = False
total_takes = 0


def threaded_client(connection, player):
    global game_round, trump, has_deck_reset, dealer, has_bidding_phase_finished, total_takes

    connection.send(pickle.dumps(players[player]))
    while True:
        try:
            data = pickle.loads(connection.recv(4048))
            players[player] = data

            # player rotating while bidding
            if players[player].bid != -1 and player == dealer and not has_all_bid():
                rotate_players()

            # extra player rotation when bidding ends
            if has_all_bid() and not has_bidding_phase_finished:
                has_bidding_phase_finished = True
                rotate_players()

            # player rotating while playing cards
            if players[player].last_played_card is not None and player == dealer:
                history.append((players[player], players[player].last_played_card))
                rotate_players()
                
            # reset history if taken hands increase
            takes = get_total_takes()
            if takes > total_takes:
                total_takes = takes
                history.clear()

            if not data:
                print("Disconnected")
                break
            else:
                cards = []
                if is_round_end():
                    if not has_deck_reset:
                        deck.reset()
                        has_deck_reset = True
                        trump = None
                        game_round += 1
                        has_bidding_phase_finished = False
                        for pl in players:
                            pl.bid = -1
                    for _ in range(game_round):
                        cards.append(deck.deal_card())

                if sum(len(hand.cards) for hand in players) == game_round * 4 and trump is None:
                    trump = deck.deal_card()

                relative_players = (players[(player + 1) % 4], players[(player + 2) % 4], players[(player + 3) % 4])
                connection.sendall(pickle.dumps((relative_players, cards, trump, dealer == player, history)))
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    connection.close()


current_player = 0
initial_deal()
dealer = random.randint(0, 3)
while True:
    connection, address = s.accept()
    print(f"Connected to {address}")

    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1
