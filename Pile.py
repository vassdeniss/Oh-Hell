import pygame
import random
import loader
from constants import WINDOW_WIDTH, WINDOW_HEIGHT


class Pile:
    def __init__(self):
        self.cards = {}

    def add(self, card):
        if f'{card.rank}{card.suit}' not in self.cards:
            card.angle = random.randint(-60, 60)
            self.cards[f'{card.rank}{card.suit}'] = card
            return True
        return False

    def clear(self):
        self.cards.clear()

    def draw(self, surface):
        for card in self.cards.values():
            card_image = pygame.transform.rotate(loader.get_card(card.rank, card.suit), card.angle)
            rect = card_image.get_rect()
            surface.blit(card_image, ((WINDOW_WIDTH - rect.width) / 2, (WINDOW_HEIGHT - rect.height) / 2))
