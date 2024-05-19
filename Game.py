from collections import deque
from random import randint

from Deck import Deck
from Hand import Hand
from drawing import draw_info


class Game:
    def __init__(self):
        self.ready = False
        self.deck = Deck()
        self.trump = None

        player_one = Hand(0)
        player_two = Hand(1)
        player_three = Hand(2)
        player_four = Hand(3)

        self.players = [player_one, player_two, player_three, player_four]

        self.initial_deal()

        self.history = deque()
        self.current = randint(0, 3)

    def is_current(self, player):
        return self.current == player

    def get_cards(self, player):
        return self.players[player]

    def does_current_player_bid(self, player):
        return self.current == player and self.players[player].bid == -1

    def has_all_bid(self):
        return all(player.bid != -1 for player in self.players)

    def bid(self, index, amount):
        self.players[index].bid = amount
        self.current = (self.current + 1) % 4

    def play(self, player, card):
        card = self.players[player].get_card(card)

        self.players[player].last_played_card = card
        self.players[player].remove_card(card)
        self.history.append((self.players[player], self.players[player].last_played_card))
        self.players[player].update_playable_cards(self.history[0][1])
        self.players[player].set_unplayable_cards()
        self.players[player].update_card_indices()
        self.current = (self.current + 1) % 4

    def initial_deal(self):
        for hand in self.players:
            hand.add_card(self.deck.deal_card())
        self.trump = self.deck.deal_card()
