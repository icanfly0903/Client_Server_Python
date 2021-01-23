# -*- coding: utf-8 -*-
import socket

def choose_server():
    global SERVER_ADDRESS
    SERVER_ADDRESS = input("Please choose Server address: ")
    
    global PORT
    PORT = int(input("Please choose the port number: "))

def create_client():
    print("Opening socket...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) # create client socket
    server_address = (SERVER_ADDRESS, PORT)
    print(f"Connecting to {str(server_address)} server")
    client.connect(server_address)

    while True:
        try:
            while True:
                # Send msg to Server
                msg = input("> ")
                if msg != "":
                    print("Send:", msg)
                    client.send(msg.encode('utf8'))
                    if msg == "quit":
                        print('Shutting down')
                        break

                # Receive data from Server
                data = client.recv(4096).decode("utf8")
                print("Server:", data)
        finally:
            client.close()
            break

if __name__ == "__main__":
    choose_server()
    create_client()
