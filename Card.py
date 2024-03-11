import pygame
import loader


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.is_face_up = False
        self.clickable_rect = None

    def flip(self):
        self.is_face_up = not self.is_face_up

    def draw(self, surface, coords, vertical=False, should_hide=False):
        image = loader.get_card(self.rank, self.suit) if not should_hide else loader.get_card('back', 'back')
        image = image if not vertical else pygame.transform.rotate(image, 90)

        self.clickable_rect = pygame.Rect(coords[0], coords[1], image.get_rect().width - 70, image.get_rect().height)
        if self.is_face_up and self.clickable_rect.collidepoint(pygame.mouse.get_pos()):
            coords = (coords[0], coords[1] - 20)

        surface.blit(image, coords)

    def handle_event(self):
        if self.clickable_rect.collidepoint(pygame.mouse.get_pos()):
            return self
