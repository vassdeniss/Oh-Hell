import random

import pygame
import sys

import loader
from Deck import Deck
from Hand import Hand
from Stack import Stack
from network import Network

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

GREEN = (39, 119, 20)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Oh Hell")

deck = Deck()

game_round = 7

player_one = Hand()
player_two = Hand()
player_three = Hand()
player_four = Hand()

PLAYERS = [player_one, player_two, player_three, player_four]

main_player = player_one
current_player = player_one

stack = Stack(WINDOW_WIDTH, WINDOW_HEIGHT)


def deal_round(hands):
    for hand in hands:
        for i in range(game_round):
            hand.add_card(deck.deal_card())
        hand.sort_cards_by_suit_and_rank()


def round_end(hands):
    # for hand in hands:
    if len(hands[0].cards) > 0:
        return False

    return True


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

        (player_two, player_three, player_four) = n.send(player)

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
            deal_round((player, player_two, player_three, player_four))
            trump = deck.deal_card()
            round_start = False

        if selected_card is not None:
            stack.add_to_stack(selected_card)
            current_player.remove_card(selected_card)

        deck.draw_trump(trump, window)

        player.draw(window, 300, 700)
        player_two.draw(window, 50, 250, vertical=True, should_hide=True)
        player_three.draw(window, 300, 50, should_hide=True)
        player_four.draw(window, 1000, 250, vertical=True, should_hide=True)

        stack.draw(window)

        if round_end((player, player_two, player_three, player_four)):
            round_start = True
            next_round()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
