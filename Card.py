import pygame
import loader
from constants import DEFAULT_SPACING


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.is_dark = False

    def get_power(self, trump_suit):
        worded_ranks = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

        power = worded_ranks[self.rank] if self.rank in worded_ranks else int(self.rank)
        if self.suit == trump_suit:
            power += 100

        return power

    def draw(self, surface, coords, is_dealer, is_last):
        image = loader.get_card(self.rank, self.suit)

        width = image.get_rect().width if is_last else DEFAULT_SPACING
        rect = pygame.Rect(coords[0], coords[1], width, image.get_rect().height)
        if not self.is_dark and rect.collidepoint(pygame.mouse.get_pos()) and is_dealer:
            image = loader.get_card(self.rank, self.suit)
            coords = (coords[0], coords[1] - 20)
        if self.is_dark or not is_dealer:
            image = loader.get_dark_card(self.rank, self.suit)

        surface.blit(image, coords)

    def draw_blank(self, surface, coords, vertical):
        image = loader.get_card('back', 'back')
        image = image if not vertical else pygame.transform.rotate(image, 90)
        surface.blit(image, coords)

    def handle_event(self, image_width, image_height, index, is_last):
        width = image_width if is_last else DEFAULT_SPACING
        rect = pygame.Rect(300 + index * DEFAULT_SPACING, 700, width, image_height)
        if rect.collidepoint(pygame.mouse.get_pos()) and not self.is_dark:
            return self

    def __str__(self):
        return f"{self.rank}{self.suit}"
