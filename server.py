# -*- coding: utf-8 -*-
import socket

def get_info():
    global PORT 
    PORT = int(input("Please choose the port number: "))

    global HOST_NAME
    HOST_NAME = socket.gethostname()

    global HOST_ADDRESS
    HOST_ADDRESS = socket.gethostbyname(HOST_NAME)

    print(HOST_NAME)
    print(HOST_ADDRESS)

def create_server():
    print("Openning socket...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) # create server socket
    server.bind((HOST_ADDRESS,PORT))
    server.listen(5)

    while True:
        client_connection, client_addr = server.accept()
        try:
            print("Connected to Client", client_addr)
            while True:
                # Receive data from Client
                data = client_connection.recv(4096)
                if not data:
                    break
                else:
                    print("-" * 20)
                    print("Client:", data.decode("utf8"))
                    if data.decode("utf8") == "quit":
                        break

                # Send msg to Client
                msg = input("Server: ")
                client_connection.send(msg.encode("utf8"))
        finally:
            client_connection.close()
            break
    print("-" * 20)
    print("Shutting dowm....")
    server.close()
    print("Done")

if __name__ == "__main__":
    get_info()
    create_server()