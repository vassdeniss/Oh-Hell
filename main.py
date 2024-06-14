import pygame
import sys
import loader
from Network import Network
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from drawing import draw_deck, draw_played_cards, draw_players_info, draw_player_cards, draw_trump, \
    draw_winner

pygame.init()
pygame.mixer.init()

DARK_BLUE = (6, 36, 72)
GRAY = (128, 128, 128)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Oh Hell!")

bid_text = ''
play_card = pygame.mixer.Sound("./sounds/play_card.wav")


def main():
    global bid_text

    loader.load_cards()

    n = Network()
    player = int(n.get_player())
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(60)
        window.fill(DARK_BLUE)

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

        selected_card = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game.is_current(
                    player) and game.has_all_bid():
                cards = game.get_cards(player)
                for i, card in enumerate(cards):
                    image = loader.get_card(card.rank, card.suit)
                    selected_card = card.handle_event(image.get_rect().width, image.get_rect().height, i,
                                                      i == len(cards) - 1)
                    if selected_card is not None:
                        break
            if event.type == pygame.KEYDOWN and game.does_current_player_bid(player):
                if event.key == pygame.K_RETURN and bid_text:
                    n.send(f"bid;{bid_text}")
                    bid_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    bid_text = bid_text[:-1]
                elif bid_text != "0" and event.unicode.isdigit() and int(bid_text + event.unicode) <= game.round:
                    total_number = int(bid_text + event.unicode)
                    if total_number > game.round:
                        continue
                    if 5 <= game.round == total_number + game.get_total_bids(player): 
                        continue
                    bid_text += event.unicode

        if game.winner is not None:
            draw_winner(window, game.winner)
            pygame.display.flip()
            continue

        draw_deck(window, len(game.deck))

        if game.does_current_player_bid(player):
            pygame.draw.rect(window, GRAY, pygame.Rect(300, 600, 50, 32))
            text_surface = pygame.font.Font(None, 32).render(bid_text, True, (255, 255, 255))
            window.blit(text_surface, (305, 605))

        if selected_card is not None:
            n.send(f"play;{str(selected_card)}")
            play_card.play()

        draw_trump(window, game.trump)
        draw_player_cards(window, game.players, player, game.is_current(player))
        draw_players_info(window, game.players, player)
        draw_played_cards(window, game.get_played_cards(player))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
