import pygame

import random

import loader


class Stack:
    def __init__(self, width, height):
        self.cards = []
        self.x = width
        self.y = height

    def add_to_stack(self, card):
        self.cards.append(self.__rotate_card(card))

    def clear(self):
        self.cards.clear()

    def draw(self, surface):
        for card in self.cards:
            rect = card.get_rect()
            surface.blit(card, ((self.x - rect.width) / 2, (self.y - rect.height) / 2))

    def __rotate_card(self, card):
        angle = random.randint(-60, 60)
        return pygame.transform.rotate(loader.get_card(card.rank, card.suit), angle)
