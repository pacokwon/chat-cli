import socket
import errno
import sys

HEADER_SIZE = 10
HOST = "127.0.0.1"
PORT = 1234

def main():
    while True:
        username = input("Enter Username: ")
        if username:
            break
        else:
            print("Invalid username!")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setblocking(False)
    client.connect((HOST, PORT))

    send_message(client, username)

    while True:
        message = input(f"{username}> ")

        if not message:
            while True:
                message = receive_message(client)
                if message is False:
                    break
                print(f"{message[0]> message[1]}")
            continue

        message = send_message(client, message)

def receive_message(client):
    try:
        user_len = int(client.recv(HEADER_SIZE).decode('utf-8'))
        user = client.recv(user_len).decode('utf-8')
        message_len = int(client.recv(HEADER_SIZE).decode('utf-8'))
        message = client.recv(message_len).decode('utf-8')

        return user, message
    except IOError as e:
        if e.error != errno.EWOULDBLOCK and e.error != errno.EAGAIN:
            print("IOError occurred!")
            print(e)
            sys.exit()
        return False

    except Exception as e:
        print("Exception occurred!")
        print(e)
        sys.exit()

def send_message(client, data):
    client.send(f"{len(data):<{HEADER_SIZE}}".encode('utf-8') + data.encode('utf-8'))

if __name__ == "__main__":
    main()

