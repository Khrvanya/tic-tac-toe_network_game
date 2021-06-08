import socket
from _thread import *
import pickle
from game import Game

server = "192.168.1.203"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as error:
    str(error)

s.listen(2)
print("Waiting for a connection, Server Started")

games = {}
PLAYERS_NUM = 0


def threaded_client(conn, p, gameId):
    global PLAYERS_NUM
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.reset_cells()

                    elif data != "get":
                        data = int(data)  # if not get then number
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    PLAYERS_NUM -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    PLAYERS_NUM += 1
    player = 0
    gameId = max(list(games)) if list(games) else 0
    if PLAYERS_NUM % 2 == 1:
        gameId += 1
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        player = 1

    start_new_thread(threaded_client, (conn, player, gameId))
