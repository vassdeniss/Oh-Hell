import pygame
import sys

import loader
from Deck import Deck
from Stack import Stack
from Network import Network

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

GREEN = (39, 119, 20)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Oh Hell")

deck = Deck()

game_round = 2

stack = Stack(WINDOW_WIDTH, WINDOW_HEIGHT)


def deal_round(hand):
    global game_round

    for _ in range(game_round):
        hand.add_card(deck.deal_card())
    hand.sort_cards_by_suit_and_rank()
    game_round += 1


def next_round():
    global game_round

    game_round += 1
    deck.reset()
    stack.clear()


def main():
    global game_round

    loader.load_cards()

    n = Network()
    player = n.get_player()
    clock = pygame.time.Clock()

    running = True
    round_start = True
    trump = None

    while running:
        clock.tick(60)

        (player_two, player_three, player_four, should_restart_game) = n.send(player)

        if should_restart_game:
            deal_round(player)
            #trump = deck.deal_card()

        selected_card = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for card in player.cards:
                    selected_card = card.handle_event()
                    if selected_card is not None:
                        break

        window.fill(GREEN)

        deck.draw(window)

        if selected_card is not None:
            stack.add_to_stack(selected_card)
            player.remove_card(selected_card)

        # deck.draw_trump(trump, window)

        player.draw(window, 300, 700)
        player_two.draw(window, 50, 250, vertical=True, should_hide=True)
        player_three.draw(window, 300, 50, should_hide=True)
        player_four.draw(window, 1000, 250, vertical=True, should_hide=True)

        stack.draw(window)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
