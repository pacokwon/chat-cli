import socket

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
    client.connect((HOST, PORT))

    send_message(client, username)

    while True:
        message = input(f"{username}> ")

        if not message:
            continue

        send_message(client, message)

def send_message(client, data):
    client.send(f"{len(data):<{HEADER_SIZE}}".encode('utf-8') + data.encode('utf-8'))

if __name__ == "__main__":
    main()

