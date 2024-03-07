import pygame
import random

import loader
from Card import Card


def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    cards = []

    for suit in suits:
        for rank in ranks:
            cards.append(Card(rank, suit))

    random.shuffle(cards)

    return cards


class Deck:
    def __init__(self):
        self.cards = create_deck()

    def reset(self):
        self.cards = create_deck()

    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def draw(self, surface):
        surface.blit(loader.get_card('back', 'back'), (50, 50))

        font = pygame.font.Font(None, 30)
        text = font.render("Deck", True, (255, 255, 255))
        surface.blit(text, (80, 20))

    def draw_trump(self, trump, surface):
        surface.blit(loader.get_card(trump.rank, trump.suit), (100, 50))
