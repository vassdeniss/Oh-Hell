import pygame
import sys

from Card import Card
from Deck import Deck

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

GREEN = (39, 119, 20)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ohil")

deck = Deck()
ace_of_spades = Card("ace", "spades")
two_of_clubs = Card("2", "clubs")


def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(GREEN)

        deck.draw(window)
        ace_of_spades.draw(window, 300, 100)
        two_of_clubs.draw(window, 500, 100)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
