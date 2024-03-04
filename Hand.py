class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def clear(self):
        self.cards.clear()

    def draw(self, surface, x, y, spacing=10):
        for i, card in enumerate(self.cards):
            card.draw(surface, x + i * (30 + spacing), y)
