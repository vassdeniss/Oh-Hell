import pygame.font
from constants import WINDOW_WIDTH


class Hand:
    def __init__(self, id):
        self.cards = []
        self.last_played_card = None
        self.bid = -1
        self.taken_hands = 0
        self.id = id
        self.score = 0

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def playable_cards(self, first_played_card, trump):
        if not first_played_card:
            return self.cards

        suit_match = [card for card in self.cards if card.suit == first_played_card.suit]
        if len(suit_match) != 0:
            return suit_match

        # trump_suit_match = [card for card in self.cards if card.suit == trump.suit]
        # if len(trump_suit_match) != 0:
        #     return trump_suit_match

        return self.cards

    def draw(self, surface, x, y, trump, is_dealer=False, spacing=10, vertical=False, should_hide=False,
             first_played_card=None):
        for i, card in enumerate(self.cards):
            card.is_face_up = not should_hide
            modified_coords = \
                (
                    x if vertical else x + i * (30 + spacing),
                    y + i * (20 + spacing) if vertical else y
                )
            card.draw(surface, modified_coords, self.playable_cards(first_played_card, trump), vertical, should_hide)
        if is_dealer:
            text = pygame.font.Font(None, 32).render("Your turn" if self.bid != -1 else "Enter bid", True,
                                                     (255, 255, 255))
            surface.blit(text, (WINDOW_WIDTH / 2 - 100, y - 150))

    def sort_cards_by_suit_and_rank(self):
        if len(self.cards) < 2:
            return None

        suit_order = {'Hearts': 0, 'Spades': 1, 'Diamonds': 2, 'Clubs': 3}
        rank_order = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'Jack': 9, 'Queen': 10,
                      'King': 11, 'Ace': 12}

        self.cards.sort(key=lambda card: (suit_order[card.suit], rank_order[card.rank]))

    def __str__(self):
        return f'B: {str(self.bid)}; T: {str(self.taken_hands)}; S: {str(self.score)}'
