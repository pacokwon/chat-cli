import socket
import select

HEADER_SIZE = 10
HOST = "127.0.0.1"
PORT = 1234

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    sockets_list = [server]
    clients = {}

    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])

        for sock in read_sockets:
            if sock == server:
                client, addr = sock.accept()
                sockets_list.append(client)
                user = receive_message(client)
                clients[client] = user
                print(f"{user['data'].decode('utf-8')} has connected")
            else:
                message = receive_message(sock)

                if message is False:
                    print(f"{clients[sock]['data'].decode('utf-8')} has disconnected")
                    sockets_list.remove(sock)
                    del clients[sock]
                    continue

                print(f"{clients[client]['data'].decode('utf-8')}> {message['data'].decode('utf-8')}")


def receive_message(client):
    try:
        message_len = client.recv(HEADER_SIZE)

        if not len(message_len):
            return False

        message_len = int(message_len.decode("utf-8"))
        return {
            "header": message_len,
            "data": client.recv(message_len)
        }
    except:
        return False

def send_message(client, user, data):
    message = f"{len(user['data']):<{HEADER_SIZE}}".encode('utf-8') + user['data']
    message += f"{len(data):<{HEADER_SIZE}}".encode('utf-8') + data
    client.send(message)

if __name__ == "__main__":
    main()

