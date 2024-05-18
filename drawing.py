import pygame
import loader
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, CARD_WIDTH, CARD_HEIGHT


def draw_deck(window):
    window.blit(loader.get_card('back', 'back'), (50, 50))
    text = pygame.font.Font(None, 32).render("Deck", True, (255, 255, 255))
    window.blit(text, (80, 20))


def draw_info(player, surface, coords):
    if player.bid == -1:
        return
    text = pygame.font.Font(None, 32).render(str(player), True, (255, 255, 255))
    surface.blit(text, coords)


def draw_played_cards(surface, cards):
    center_x = WINDOW_WIDTH / 2 - CARD_WIDTH / 2
    center_x_vertical = WINDOW_WIDTH / 2 - CARD_HEIGHT / 2
    center_y = WINDOW_HEIGHT / 2 - CARD_HEIGHT / 2
    center_y_vertical = WINDOW_HEIGHT / 2 - CARD_WIDTH / 2

    player_positions = [
        (center_x, center_y + CARD_HEIGHT / 2 + 10),  # bottom
        (center_x_vertical - CARD_HEIGHT / 2 - 10, center_y_vertical),  # left
        (center_x, center_y - CARD_HEIGHT / 2 - 10),  # top
        (center_x_vertical + CARD_HEIGHT / 2 + 10, center_y_vertical)  # right
    ]

    for i, card in enumerate(cards):
        if card is None:
            continue

        image = loader.get_card(card.rank, card.suit)

        card_x, card_y = player_positions[i]
        if i == 1:
            image = pygame.transform.rotate(image, -90)
        elif i == 3:
            image = pygame.transform.rotate(image, 90)
        elif i == 2:
            image = pygame.transform.rotate(image, 180)

        surface.blit(image, (card_x, card_y))
