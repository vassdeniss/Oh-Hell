import pygame.font
from constants import WINDOW_WIDTH


class Hand:
    def __init__(self, id):
        self.cards = []
        self.playable_cards = self.get_playable_cards()
        self.last_played_card = None
        self.bid = -1
        self.taken_hands = 0
        self.id = id
        self.score = 0

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        self._current_index = 0
        return self

    def __next__(self):
        if self._current_index < len(self.cards):
            card = self.cards[self._current_index]
            self._current_index += 1
            return card
        else:
            raise StopIteration

    def get_card(self, identifier):
        for card in self.playable_cards:
            if str(card) == identifier:
                return card

    def add_card(self, card):
        card.index = len(self.cards)
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def reset(self):
        self.last_played_card = None
        self.score += self.bid * self.bid + 10 if self.bid == self.taken_hands else 0
        self.bid = -1
        self.taken_hands = 0

    def update_playable_cards(self, first_played_card):
        self.playable_cards = self.get_playable_cards(first_played_card)

    def update_card_indices(self):
        for i, card in enumerate(self.cards):
            card.index = i

    def set_unplayable_cards(self):
        for card in self.cards:
            if card not in self.playable_cards:
                card.is_dark = True

    def get_playable_cards(self, first_played_card=None):
        if not first_played_card:
            return self.cards

        suit_match = [card for card in self.cards if card.suit == first_played_card.suit]
        if len(suit_match) != 0:
            return suit_match

        return self.cards

    def draw(self, surface, x, y, is_dealer, spacing=10):
        for i, card in enumerate(self.cards):
            card.draw(surface, (x + i * (30 + spacing), y), is_dealer)
        if is_dealer:
            text = pygame.font.Font(None, 32).render("Your turn" if self.bid != -1 else "Enter bid", True,
                                                     (255, 255, 255))
            surface.blit(text, (WINDOW_WIDTH / 2 - 100, y - 150))

    def draw_blanks(self, surface, x, y, vertical, spacing=10):
        for i, card in enumerate(self.cards):
            modified_coords = \
                (
                    x if vertical else x + i * (30 + spacing),
                    y + i * (20 + spacing) if vertical else y
                )
            card.draw_blank(surface, modified_coords, vertical)

    def sort_cards_by_suit_and_rank(self):
        if len(self.cards) < 2:
            return None

        suit_order = {'Hearts': 0, 'Spades': 1, 'Diamonds': 2, 'Clubs': 3}
        rank_order = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'Jack': 9, 'Queen': 10,
                      'King': 11, 'Ace': 12}

        self.cards.sort(key=lambda card: (suit_order[card.suit], rank_order[card.rank]))

    def __str__(self):
        return f'B: {str(self.bid)}; T: {str(self.taken_hands)}; S: {str(self.score)}'
