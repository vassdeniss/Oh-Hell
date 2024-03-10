import pygame

import random

import loader


class Pile:
    def __init__(self, width, height):
        self.cards = {}
        self.x = width
        self.y = height

    def add(self, card):
        if f'{card.rank}{card.suit}' not in self.cards:
            card.angle = random.randint(-60, 60)
            self.cards[f'{card.rank}{card.suit}'] = card

    def clear(self):
        self.cards.clear()

    def draw(self, surface):
        for card in self.cards.values():
            card_image = pygame.transform.rotate(loader.get_card(card.rank, card.suit), card.angle)
            rect = card_image.get_rect()
            surface.blit(card_image, ((self.x - rect.width) / 2, (self.y - rect.height) / 2))
