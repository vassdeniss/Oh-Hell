import random

import pygame
import sys

from Deck import Deck
from Hand import Hand
from Stack import Stack

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

GREEN = (39, 119, 20)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Oh Hell")

deck = Deck()

game_round = 7

player_one = Hand((300, 700))
player_two = Hand((50, 250))
player_three = Hand((1000, 250))
player_four = Hand((300, 50))

main_player = player_one
current_player = player_one

stack = Stack(WINDOW_WIDTH, WINDOW_HEIGHT)


def deal_round(hands):
    for hand in hands:
        for i in range(game_round):
            hand.add_card(deck.deal_card())
        hand.sort_cards_by_suit_and_rank()


def round_end():
    return False
    # check if empty hands on all players


def next_round():
    global game_round

    game_round += 1
    deck.reset()
    stack.clear()


def main():
    global game_round

    running = True
    round_start = True
    trump = None

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
            trump = deck.deal_card()
            round_start = False

        if selected_card is not None:
            stack.add_to_stack(selected_card)
            current_player.remove_card(selected_card)

        deck.draw_trump(trump, window)

        player_one.draw(window)
        player_two.draw(window, vertical=True, should_hide=True)
        player_three.draw(window, vertical=True, should_hide=True)
        player_four.draw(window, should_hide=True)

        stack.draw(window)

        if round_end():
            round_start = True
            next_round()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
