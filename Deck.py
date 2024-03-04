import pygame
import random

from Card import Card
from Util import get_card_image


class Deck:
    def __init__(self):
        self.cards = self.__create_deck()
        self.shuffle()

    def __create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        cards = []

        for suit in suits:
            for rank in ranks:
                cards.append(Card(rank, suit))

        return cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, surface):
        surface.blit(get_card_image(), (50, 50))

        font = pygame.font.Font(None, 30)
        text = font.render("Deck", True, (255, 255, 255))
        surface.blit(text, (80, 20))

    def deal_card(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

    def test(self):
        for card in self.cards:
            print(f'{card.rank} - {card.suit}')
