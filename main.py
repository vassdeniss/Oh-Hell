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


def draw_info(bid, taken, surface, x, y):
    if bid == -1:
        return
    text = pygame.font.Font(None, 32).render(f'Bid: {str(bid)}; Taken: {str(taken)}', True, (255, 255, 255))
    surface.blit(text, (x, y))
    

def get_first_played_card(hands):
    global first_played_card

    if first_played_card is not None:
        return first_played_card

    for hand in hands:
        if hand.last_played_card is not None:
            first_played_card = hand.last_played_card
            return first_played_card

    return None


def get_best_player(history, trump_suit):
    best_player = None
    best_player_power = 0
    while history:
        (player, card) = history.popleft()
        power = card.get_power(trump_suit)
        if power > best_player_power:
            best_player_power = power 
            best_player = player
    return best_player


bid_text = ''
total_cards_in_hand_per_round = 1
first_played_card = None
backup_trump_suit = None


def main():
    global bid_text, backup_trump_suit

    loader.load_cards()

    n = Network()
    player = n.get_player()
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)

        (players, cards, trump, is_dealer, history) = n.send(player)
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
            backup_trump_suit = trump.suit
            window.blit(loader.get_card(trump.rank, trump.suit), (100, 50))

        first_card = get_first_played_card((player, player_four, player_three, player_two))

        if len(history) >= 4:
            player.last_played_card = None
            best_player = get_best_player(history, trump.suit if trump is not None else backup_trump_suit)
            if best_player.id == player.id:
                print('player is best')
                player.taken_hands += 1

        player.draw(window, 300, 700, is_dealer=is_dealer, first_played_card=first_card, trump=trump)
        player_two.draw(window, 50, 250, vertical=True, should_hide=True,
                        first_played_card=first_card, trump=trump)
        player_three.draw(window, 300, 50, should_hide=True, first_played_card=first_card,
                          trump=trump)
        player_four.draw(window, 1000, 250, vertical=True, should_hide=True,
                         first_played_card=first_card, trump=trump)

        draw_info(player.bid, player.taken_hands, window, 300, 600)
        draw_info(player_two.bid, player_two.taken_hands, window, 50, 220)
        draw_info(player_three.bid, player_three.taken_hands, window, 300, 210)
        draw_info(player_four.bid, player_fouraken_hands, window, 1000, 210)

        draw_played_cards(window, (player.last_played_card, player_two.last_played_card, player_three.last_played_card,
                                   player_four.last_played_card))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
