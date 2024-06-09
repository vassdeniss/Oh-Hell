from collections import deque
from random import randint

from Deck import Deck
from Hand import Hand


class Game:
    def __init__(self):
        self.ready = False
        self.deck = Deck()
        self.round = 1
        self.round_repeats = 0
        self.players = [Hand(0, self.deck.deal_card()), Hand(1, self.deck.deal_card()), Hand(2, self.deck.deal_card()), Hand(3, self.deck.deal_card())]
        self.trump = self.deck.deal_card()
        self.history = deque()
        self.current = randint(0, 3)
        self.winner = None

    def is_current(self, player):
        return self.current == player

    def get_cards(self, player):
        return self.players[player]

    def get_played_cards(self, player):
        return (self.players[player].last_played_card, self.players[(player + 1) % 4].last_played_card,
                self.players[(player + 2) % 4].last_played_card,
                self.players[(player + 3) % 4].last_played_card)

    def does_current_player_bid(self, player):
        return self.current == player and self.players[player].bid == -1

    def has_all_bid(self):
        return all(player.bid != -1 for player in self.players)

    def bid(self, index, amount):
        self.players[index].bid = int(amount)
        self.current = (self.current + 1) % 4

    def play(self, player, card):
        card = self.players[player].get_card(card)

        self.players[player].last_played_card = card
        self.players[player].remove_card(card)
        self.history.append((player, self.players[player].last_played_card))
        for player in self.players:
            player.update_playable_cards(self.history[0][1])
        self.current = (self.current + 1) % 4

    def check_for_takes(self):
        if len(self.history) >= 4:
            for player in self.players:
                player.last_played_card = None
                player.update_playable_cards()
            index = self._get_best_player()
            self.players[index].taken_hands += 1
            self.current = index

    def check_end_round(self):
        if all(len(player) == 0 for player in self.players):
            self.history.clear()
            self.deck.reset()
            self.round += 1 if self.round < 13 else 0
            self.round_repeats += 1 if self.round == 13 else 0
            for player in self.players:
                for _ in range(self.round):
                    player.add_card(self.deck.deal_card())
                player.sort_cards_by_suit_and_rank()
                player.update_playable_cards()
                player.reset()
            self.trump = self.deck.deal_card() if self.round < 13 else None

    def check_game_over(self):
        if self.round_repeats == 5:
            scores = [player.score for player in self.players]
            max_score = max(scores)
            self.winner = f'Winner is: Player {scores.index(max_score) + 1} with {max_score} score'

    def _get_best_player(self):
        best_player = None
        best_player_power = 0
        while self.history:
            (player, card) = self.history.popleft()
            power = card.get_power(self.trump.suit)
            if power > best_player_power:
                best_player_power = power
                best_player = player
        return best_player
