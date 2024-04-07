import pygame
import sys

import loader
from Network import Network
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, CARD_WIDTH, CARD_HEIGHT

pygame.init()

GREEN = (39, 119, 20)
GRAY = (128, 128, 128)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Oh Hell!")


def has_all_bid(bids):
    return all(bid != -1 for bid in bids)


def is_last_bid(bids):
    return bids[0] == -1 and all(bid != -1 for bid in bids[1:])


def deal_round(cards, hand):
    global total_cards_in_hand_per_round

    for i in range(len(cards)):
        hand.add_card(cards[i])
    hand.sort_cards_by_suit_and_rank()
    total_cards_in_hand_per_round += 1


def draw_deck():
    window.blit(loader.get_card('back', 'back'), (50, 50))
    text = pygame.font.Font(None, 32).render("Deck", True, (255, 255, 255))
    window.blit(text, (80, 20))


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


def draw_bid(bid, surface, x, y):
    if bid == -1:
        return
    text = pygame.font.Font(None, 32).render(str(bid), True, (255, 255, 255))
    surface.blit(text, (x, y))


bid_text = ''
total_cards_in_hand_per_round = 5


def main():
    global bid_text

    loader.load_cards()

    n = Network()
    player = n.get_player()
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)

        (players, cards, trump, is_dealer) = n.send(player)
        (player_two, player_three, player_four) = players

        if len(cards) > 0:
            deal_round(cards, player)
            player.last_played_card = None
            player.bid = -1

        selected_card = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_dealer and has_all_bid(
                    (player.bid, player_two.bid, player_three.bid,
                     player_four.bid)):
                for card in player.cards:
                    selected_card = card.handle_event()
                    if selected_card is not None:
                        break
            if event.type == pygame.KEYDOWN and player.bid == -1:
                if event.key == pygame.K_RETURN and bid_text:
                    if (is_last_bid((player.bid, player_two.bid, player_three.bid, player_four.bid))
                            and total_cards_in_hand_per_round == 5):
                        total = sum((player_two.bid, player_three.bid, player_four.bid))
                        if int(bid_text) + total == total_cards_in_hand_per_round:
                            continue

                    player.bid = int(bid_text)
                    bid_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    bid_text = bid_text[:-1]
                elif bid_text != "0" and event.unicode.isdigit():
                    if int(bid_text + event.unicode) <= total_cards_in_hand_per_round:
                        bid_text += event.unicode

        window.fill(GREEN)

        draw_deck()

        if player.bid == -1 and is_dealer:
            pygame.draw.rect(window, GRAY, pygame.Rect(300, 600, 50, 32))
            text_surface = pygame.font.Font(None, 32).render(bid_text, True, (255, 255, 255))
            window.blit(text_surface, (305, 605))

        if selected_card is not None:
            player.last_played_card = selected_card
            player.remove_card(selected_card)

        if trump is not None:
            window.blit(loader.get_card(trump.rank, trump.suit), (100, 50))

        player.draw(window, 300, 700, is_dealer, last_played_card=player_four.last_played_card)
        player_two.draw(window, 50, 250, vertical=True, should_hide=True, last_played_card=player_four.last_played_card)
        player_three.draw(window, 300, 50, should_hide=True, last_played_card=player_four.last_played_card)
        player_four.draw(window, 1000, 250, vertical=True, should_hide=True, last_played_card=player_four.last_played_card)

        draw_bid(player.bid, window, 300, 600)
        draw_bid(player_two.bid, window, 50, 220)
        draw_bid(player_three.bid, window, 300, 210)
        draw_bid(player_four.bid, window, 1000, 220)

        draw_played_cards(window, (player.last_played_card, player_two.last_played_card, player_three.last_played_card,
                                   player_four.last_played_card))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
