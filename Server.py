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

s.listen()
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
