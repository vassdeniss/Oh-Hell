class Hand:
    def __init__(self, coords):
        self.cards = []
        self.coords = coords

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def clear(self):
        self.cards.clear()

    def draw(self, surface, spacing=10, vertical=False, should_hide=False, is_main_deck=False):
        for i, card in enumerate(self.cards):
            modified_coords = \
                (
                    self.coords[0] if vertical else self.coords[0] + i * (30 + spacing),
                    self.coords[1] + i * (20 + spacing) if vertical else self.coords[1]
                )
            card.draw(surface, modified_coords, vertical, should_hide, is_main_deck)

    def sort_cards_by_suit_and_rank(self):
        if len(self.cards) < 2:
            return None

        suit_order = {'Hearts': 0, 'Spades': 1, 'Diamonds': 2, 'Clubs': 3}
        rank_order = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'Jack': 9, 'Queen': 10,
                      'King': 11, 'Ace': 12}

        def card_sort_key(card):
            return suit_order[card.suit], rank_order[card.rank]

        self.cards.sort(key=card_sort_key)
