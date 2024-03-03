import pygame


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.front_image = self.__get_card_image()
        #self.back_image = back_image
        self.is_face_up = False

    def flip(self):
        self.is_face_up = not self.is_face_up

    def draw(self, surface, x, y):
        #surface.blit(self.front_image if self.is_face_up else self.back_image, (x, y))
        surface.blit(self.front_image, (x, y))

    def __get_card_image(self):
        image = pygame.image.load(f'./cards/{self.rank}_of_{self.suit}.png')
        return pygame.transform.scale(image, (105, 150))
