import pygame
from Util import get_card_image


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.front_image = get_card_image(self.rank, self.suit)
        self.back_image = get_card_image()
        self.is_face_up = False

    def flip(self):
        self.is_face_up = not self.is_face_up

    def draw(self, surface, coords, vertical=False, should_hide=False):
        image = self.front_image if not should_hide else self.back_image
        image = image if not vertical else pygame.transform.rotate(image, 90)

        surface.blit(image, coords)
