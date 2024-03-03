import pygame


def get_card_image(rank='back', suit=None):
    name = f'{rank}_of_{suit.lower()}' if suit else 'back'
    image = pygame.image.load(f'./cards/{name}.png')
    return pygame.transform.scale(image, (105, 150))
