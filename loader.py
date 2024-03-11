import os
import pygame
from constants import CARD_WIDTH, CARD_HEIGHT

cards = {}


def get_card(rank, suit):
    name = f'{rank.lower()}_of_{suit.lower()}'
    return cards[name]


def load_cards():
    for filename in os.listdir('./cards'):
        card_name = os.path.splitext(filename)[0]
        image = pygame.image.load(os.path.join('./cards', filename)).convert_alpha()
        cards[card_name] = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
