import pickle
import socket
from _thread import start_new_thread

from Game import Game
from constants import LOCAL_IP, PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((LOCAL_IP, PORT))
except socket.error as err:
    str(err)

s.listen(4)
print("Server started, waiting for connections...")

games = {}
idCount = 0


def threaded_client(connection, player, gameId):
    global idCount
    connection.send(str.encode(str(player)))

    while True:
        try:
            data = connection.recv(4096).decode()
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    (command, payload) = data.split(';')
                    if command == "bid":
                        game.bid(player, payload)
                    elif command == "play":
                        game.play(player, payload)
                    game.check_for_takes()
                    game.check_end_round()
                    game.check_game_over()
                    connection.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection...")
    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass

    idCount -= 1
    connection.close()

    #     try:
    #         # update takes
    #         old_total_takes = total_takes
    #         total_takes = sum(player.taken_hands for player in players)
    #         if total_takes > old_total_takes:
    #             history.clear()
    #         
    # 
    #         # game over
    #         # if winner_info:
    #         #     relative_players = (players[(player + 1) % 4], players[(player + 2) % 4], players[(player + 3) % 4])
    #         #     connection.sendall(
    #         #         pickle.dumps((relative_players, [], trump, dealer == player, history, winner_info)))
    #         #     continu
    # 
    #         if not data:
    #             print("Disconnected")
    #             break
    #         else:
    #             cards = []
    #             if is_round_end():
    #                 if not has_deck_reset:
    #                     game_round += 1 if game_round < 13 else 0
    #                     if game_round == 13:
    #                         # last_round_repeats += 1
    #                         # if last_round_repeats == 5:
    #                         scores = [p.score for p in players]
    #                         max_score = max(scores)
    #                         winner_info = (scores.index(max_score) + 1, max_score)
    #                         continue


while True:
    connection, address = s.accept()
    print(f"Connected to {address}")

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 4
    if idCount % 4 == 1:
        games[gameId] = Game()
        print("Creating a game...")
    elif idCount % 4 == 2:
        p = 1
    elif idCount % 4 == 3:
        p = 2
    elif idCount % 4 == 0:
        games[gameId].ready = True
        p = 3

    start_new_thread(threaded_client, (connection, p, gameId))
