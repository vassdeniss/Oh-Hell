import os
import pygame
from constants import CARD_WIDTH, CARD_HEIGHT

cards = {}
dark_cards = {}


def get_card(rank, suit):
    name = f'{rank.lower()}_of_{suit.lower()}'
    return cards[name]


def get_dark_card(rank, suit):
    name = f'{rank.lower()}_of_{suit.lower()}'
    return dark_cards[name]


def load_cards():
    for filename in os.listdir('./cards'):
        card_name = os.path.splitext(filename)[0]
        image = pygame.image.load(os.path.join('./cards', filename)).convert_alpha()
        scaled = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
        cards[card_name] = scaled
        dark_cards[card_name] = make_dark_card(scaled.copy())


def make_dark_card(card):
    dark = pygame.Surface((card.get_width(), card.get_height()), flags=pygame.SRCALPHA)
    dark.fill((0, 0, 0, 70))
    card.blit(dark, (0, 0))
    return card
