import pygame
import sys

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

GREEN = (39, 119, 20)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ohil")

def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(GREEN)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
