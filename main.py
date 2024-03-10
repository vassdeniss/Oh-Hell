import pygame
import sys

import loader
from Network import Network
from constants import WINDOW_WIDTH, WINDOW_HEIGHT

pygame.init()

GREEN = (39, 119, 20)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Oh Hell")


def deal_round(cards, hand):
    for i in range(len(cards)):
        hand.add_card(cards[i])
    hand.sort_cards_by_suit_and_rank()


def draw_deck():
    window.blit(loader.get_card('back', 'back'), (50, 50))
    font = pygame.font.Font(None, 30)
    text = font.render("Deck", True, (255, 255, 255))
    window.blit(text, (80, 20))


def main():
    loader.load_cards()

    n = Network()
    player = n.get_player()
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)

        (player_two, player_three, player_four, cards, trump, pile, is_dealer) = n.send(player)

        if len(cards) > 0:
            deal_round(cards, player)
            player.last_played_card = None

        selected_card = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if is_dealer:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for card in player.cards:
                        selected_card = card.handle_event()
                        if selected_card is not None:
                            break

        window.fill(GREEN)

        draw_deck()

        if selected_card is not None:
            player.last_played_card = selected_card
            player.remove_card(selected_card)

        if trump is not None:
            window.blit(loader.get_card(trump.rank, trump.suit), (100, 50))

        player.draw(window, 300, 700, is_dealer)
        player_two.draw(window, 50, 250, vertical=True, should_hide=True)
        player_three.draw(window, 300, 50, should_hide=True)
        player_four.draw(window, 1000, 250, vertical=True, should_hide=True)

        pile.draw(window)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
