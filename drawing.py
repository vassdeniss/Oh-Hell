import pygame
import loader
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, CARD_WIDTH, CARD_HEIGHT


def draw_deck(window, deck_len):
    if deck_len == 0:
        return

    window.blit(loader.get_card('back', 'back'), (50, 50))
    text = pygame.font.Font(None, 32).render("Deck", True, (255, 255, 255))
    text_rect = text.get_rect(center=(50 + (CARD_WIDTH / 2), 30))
    window.blit(text, text_rect)


def draw_players_info(surface, players, player):
    draw_info(players[player], surface, (300, 600))
    draw_info(players[(player + 1) % 4], surface, (50, 220))
    draw_info(players[(player + 2) % 4], surface, (300, 210))
    draw_info(players[(player + 3) % 4], surface, (1000, 210))


def draw_info(player, surface, coords):
    if player.bid == -1:
        return
    text = pygame.font.Font(None, 32).render(str(player), True, (255, 255, 255))
    surface.blit(text, coords)


def draw_player_cards(surface, players, player, is_current):
    players[player].draw(surface, 300, 700, is_current)
    players[(player + 1) % 4].draw_blanks(surface, 50, 250, True)
    players[(player + 2) % 4].draw_blanks(surface, 300, 50, False)
    players[(player + 3) % 4].draw_blanks(surface, 1000, 250, True)


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
