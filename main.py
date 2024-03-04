import random

import pygame
import sys

from Deck import Deck
from Hand import Hand

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

GREEN = (39, 119, 20)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Oh Hell")

deck = Deck()

deck.test()

game_round = 13

player_one = Hand((300, 700))
player_two = Hand((50, 250))
player_three = Hand((1000, 250))
player_four = Hand((300, 50))

main_player = player_one
current_player = player_one

middle_cards = []


def deal_round(hands):
    for hand in hands:
        for i in range(game_round):
            hand.add_card(deck.deal_card())
        hand.sort_cards_by_suit_and_rank()


def main():
    running = True
    round_start = True

    while running:
        selected_card = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for card in current_player.cards:
                    selected_card = card.handle_event()
                    if selected_card is not None:
                        break

        window.fill(GREEN)

        deck.draw(window)

        if round_start:
            deal_round([player_one, player_two, player_three, player_four])
            round_start = False

        if selected_card is not None:
            angle = random.randint(-60, 60)
            rotated = pygame.transform.rotate(selected_card.front_image, angle)
            middle_cards.append(rotated)
            current_player.remove_card(selected_card)

        player_one.draw(window)
        player_two.draw(window, vertical=True, should_hide=True)
        player_three.draw(window, vertical=True, should_hide=True)
        player_four.draw(window, should_hide=True)

        for card in middle_cards:
            window.blit(card, ((1200 - card.get_rect().width) / 2, (900 - card.get_rect().height) / 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
