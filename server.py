import socket
import select

HOST = "127.0.0.1"
IP = 1234

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, IP))

if __name__ == "__main__":
    main()

