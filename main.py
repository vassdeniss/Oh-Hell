import pygame
import sys
import loader
from Network import Network
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from drawing import draw_deck, draw_info, draw_played_cards, draw_players_info, draw_player_cards, draw_trump

pygame.init()

DARK_BLUE = (6, 36, 72)
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
    total_cards_in_hand_per_round += 1 if total_cards_in_hand_per_round < 13 else 0


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
    player = int(n.get_player())
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)
        window.fill(DARK_BLUE)

        if player == -1:
            text = pygame.font.Font(None, 32).render('Waiting for server...', True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            window.blit(text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            player = int(n.connect())
            continue

        try:
            game = n.send("get;null")
        except:
            print("Couldn't get game")
            break

        if not game.ready:
            text = pygame.font.Font(None, 32).render('Waiting for players...', True, (255, 255, 255))
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            window.blit(text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            continue

        # if len(history) >= 4:
        #     player.last_played_card = None
        #     best_player = get_best_player(history, trump.suit if trump is not None else backup_trump_suit)
        #     if best_player.id == player.id:
        #         player.taken_hands += 1

        selected_card = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game.is_current(player) and game.has_all_bid():
                # TODO: use only playable?
                cards = game.get_cards(player)
                for i, card in enumerate(cards):
                    image = loader.get_card(card.rank, card.suit)
                    selected_card = card.handle_event(image.get_rect().width, image.get_rect().height, i, i == len(cards) - 1)
                    if selected_card is not None:
                        break
            if event.type == pygame.KEYDOWN and game.does_current_player_bid(player):
                if event.key == pygame.K_RETURN and bid_text:
                    # if (is_last_bid((player.bid, player_two.bid, player_three.bid, player_four.bid))
                    #         and total_cards_in_hand_per_round == 5):
                    #     total = sum((player_two.bid, player_three.bid, player_four.bid))
                    #     if int(bid_text) + total == total_cards_in_hand_per_round:
                    #         continue

                    n.send(f"bid;{bid_text}")
                    bid_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    bid_text = bid_text[:-1]
                elif bid_text != "0" and event.unicode.isdigit() and int(bid_text + event.unicode) <= game.round:
                    bid_text += event.unicode

        draw_deck(window, len(game.deck))

        if game.does_current_player_bid(player):
            pygame.draw.rect(window, GRAY, pygame.Rect(300, 600, 50, 32))
            text_surface = pygame.font.Font(None, 32).render(bid_text, True, (255, 255, 255))
            window.blit(text_surface, (305, 605))

        if selected_card is not None:
            n.send(f"play;{str(selected_card)}")

        draw_trump(window, game.trump)
        draw_player_cards(window, game.players, player, game.is_current(player))
        draw_players_info(window, game.players, player)
        draw_played_cards(window, game.get_played_cards(player))
        # if winner_info is not None:
        #     text = pygame.font.Font(None, 32).render(f'Winner is: Player {winner_info[0]} with {winner_info[1]} score', True, (255, 255, 255))
        #     text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        #     window.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
