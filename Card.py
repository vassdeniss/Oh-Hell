import pygame
import loader


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.is_face_up = False
        self.clickable_rect = None
        self.is_dark = False

    def draw(self, surface, coords, playable_cards=[], vertical=False, should_hide=False):
        image = loader.get_card(self.rank, self.suit) if not should_hide else loader.get_card('back', 'back')
        image = image if not vertical else pygame.transform.rotate(image, 90)

        self.clickable_rect = pygame.Rect(coords[0], coords[1], image.get_rect().width - 70, image.get_rect().height)
        if self.is_face_up and self in playable_cards and self.clickable_rect.collidepoint(pygame.mouse.get_pos()):
            coords = (coords[0], coords[1] - 20)

        if self.is_face_up and self not in playable_cards:
            self.is_dark = True
            surface.blit(loader.get_dark_card(self.rank, self.suit), coords)
            return

        self.is_dark = False
        surface.blit(image, coords)

    def handle_event(self):
        if self.clickable_rect.collidepoint(pygame.mouse.get_pos()) and not self.is_dark:
            return self
