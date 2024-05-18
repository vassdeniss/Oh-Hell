from collections import deque
from random import randint

from Deck import Deck
from Hand import Hand
from drawing import draw_info


class Game:
    def __init__(self):
        self.ready = False
        self.deck = Deck()

        player_one = Hand(0)
        player_two = Hand(1)
        player_three = Hand(2)
        player_four = Hand(3)

        self.players = [player_one, player_two, player_three, player_four]
        self.history = deque()
        self.current = randint(0, 3)

    def does_current_player_bid(self, player):
        return self.current == player and self.players[player].bid == -1

    def bid(self, index, amount):
        self.players[index].bid = amount
        self.current = (self.current + 1) % 4
