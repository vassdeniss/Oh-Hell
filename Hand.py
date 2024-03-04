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

    def draw(self, surface, spacing=10, vertical=False, should_hide=False):
        for i, card in enumerate(self.cards):
            modified_coords = \
                (
                    self.coords[0] if vertical else self.coords[0] + i * (30 + spacing),
                    self.coords[1] + i * (20 + spacing) if vertical else self.coords[1]
                )
            card.draw(surface, modified_coords, vertical, should_hide)
