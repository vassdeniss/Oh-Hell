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


def deal_round(hands):
    for hand in hands:
        for i in range(game_round):
            hand.add_card(deck.deal_card())


def main():
    running = True
    round_start = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(GREEN)

        deck.draw(window)

        if round_start:
            deal_round([player_one, player_two, player_three, player_four])
            round_start = False

        player_one.draw(window)
        player_two.draw(window, vertical=True, should_hide=True)
        player_three.draw(window, vertical=True, should_hide=True)
        player_four.draw(window, should_hide=True)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
