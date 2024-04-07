import pygame.font
from constants import WINDOW_WIDTH


class Hand:
    def __init__(self):
        self.cards = []
        self.last_played_card = None
        self.bid = -1

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def clear(self):
        self.cards.clear()

    def draw(self, surface, x, y, is_dealer=False, spacing=10, vertical=False, should_hide=False):
        for i, card in enumerate(self.cards):
            card.is_face_up = not should_hide
            modified_coords = \
                (
                    x if vertical else x + i * (30 + spacing),
                    y + i * (20 + spacing) if vertical else y
                )
            card.draw(surface, modified_coords, vertical, should_hide)
        if is_dealer:
            text = pygame.font.Font(None, 32).render("Your turn" if self.bid != -1 else "Enter bid", True,
                                                     (255, 255, 255))
            surface.blit(text, (WINDOW_WIDTH / 2 - 100, y - 50))

    def sort_cards_by_suit_and_rank(self):
        if len(self.cards) < 2:
            return None

        suit_order = {'Hearts': 0, 'Spades': 1, 'Diamonds': 2, 'Clubs': 3}
        rank_order = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'Jack': 9, 'Queen': 10,
                      'King': 11, 'Ace': 12}

        def card_sort_key(card):
            return suit_order[card.suit], rank_order[card.rank]

        self.cards.sort(key=card_sort_key)
