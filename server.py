import socket
from _thread import start_new_thread

server = "192.168.0.30"
port = 3000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as err:
    str(err)

s.listen(4)
print("Server started, waiting for connections...")


def threaded_client(connection):
    connection.send(str.encode("Connected"))
    reply = "192.168.0.30"
    while True:
        try:
            data = connection.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconneccted")
                break
            else:
                print(f"Received: {reply}")
                print(f"Sending: {reply}")

            connection.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    connection.close()


while True:
    connection, address = s.accept()
    print(f"Connected to {address}")

    start_new_thread(threaded_client, (connection,))
