import pygame
import sys

from Card import Card
from Deck import Deck
from Hand import Hand

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

GREEN = (39, 119, 20)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Oh Hell")

deck = Deck()
ace_of_spades = Card("ace", "spades")
two_of_clubs = Card("2", "clubs")

deck.test()

game_round = 13

player_one = Hand()


def deal_round(hand):
    for i in range(game_round):
        hand.add_card(deck.deal_card())


def main():
    running = True
    round_start = True
    cards = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(GREEN)

        deck.draw(window)

        if round_start:
            deal_round(player_one)
            round_start = False
        
        player_one.draw(window, 300, 700)

        # ace_of_spades.draw(window, 300, 100)
        # two_of_clubs.draw(window, 500, 100)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
