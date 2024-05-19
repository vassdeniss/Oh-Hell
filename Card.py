import pygame
import loader


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.is_dark = False
        self.index = -1

    def get_power(self, trump_suit):
        worded_ranks = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

        power = worded_ranks[self.rank] if self.rank in worded_ranks else int(self.rank)
        if self.suit == trump_suit:
            power += 100

        return power

    def draw(self, surface, coords, is_dealer):
        image = loader.get_card(self.rank, self.suit)

        rect = pygame.Rect(300 + self.index * (30 + 10), 700, image.get_rect().width - 70, image.get_rect().height)
        if not self.is_dark and rect.collidepoint(pygame.mouse.get_pos()) and is_dealer:
            coords = (coords[0], coords[1] - 20)

        if self.is_dark or not is_dealer:
            surface.blit(loader.get_dark_card(self.rank, self.suit), coords)
        else:
            surface.blit(image, coords)

    def draw_blank(self, surface, coords, vertical):
        image = loader.get_card('back', 'back')
        image = image if not vertical else pygame.transform.rotate(image, 90)
        surface.blit(image, coords)

    def handle_event(self, image_width, image_height):
        rect = pygame.Rect(300 + self.index * (30 + 10), 700, image_width - 70, image_height)
        if rect.collidepoint(pygame.mouse.get_pos()) and not self.is_dark:
            return self
        
    def __str__(self):
        return f"{self.rank}{self.suit}"
