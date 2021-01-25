import os
import socket
import time

PORT = 9669 # Port to connect server

def get_info():
    global HOST_NAME
    HOST_NAME = socket.gethostname()

    global HOST_ADDRESS
    HOST_ADDRESS = '127.0.0.1'
    # socket.gethostbyname(HOST_NAME)

    print("Server Name:", HOST_NAME)
    print("Server Address:", HOST_ADDRESS)

def create_server():
    print("Openning socket...")
    # create server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as server:
        server.bind((HOST_ADDRESS,PORT))
        server.listen()

        # Accepting the connection 
        client_connection, client_address = server.accept()
        print("...connected to Client", client_address)
        with client_connection:
            while True:
                # Receive request from client
                request = client_connection.recv(1024).decode("utf8")
                if request == "download":
                    print("*** Sending file to client ***")
                    # Getting file details 
                    file_name = client_connection.recv(1024).decode("utf8")
                    if not file_name:
                        break
                    else:
                        print(f"=> {file_name} is being sent to client...")
                        file_size = os.path.getsize("/Code/server/" + file_name)
                        client_connection.send(str(file_size).encode("utf8"))

                        # Openning file and sending data 
                        with open("./server/" + file_name, "rb") as f:
                            c = 0
                            # Starting the time capture 
                            start_time = time.time()

                            # Running loop while c != file_size 
                            while c <= file_size:
                                data = f.read(10240) 
                                if not data:
                                    break
                                client_connection.sendall(data)
                                c += len(data)

                            # Ending the time capture 
                            end_time = time.time()

                        print("File transfer complete. Total time:", end_time - start_time)
                    break
                    
                elif request == "upload":
                    print("*** Receiving file from client ***")
                    file_name = client_connection.recv(1024).decode("utf8")
                    file_size = client_connection.recv(1024).decode("utf8")

                    if not file_name:
                        break
                    else:
                        with open("/Code/server/" + file_name, "wb") as f:
                            print(f"=> {file_name} is being received from client ...")
                            c = 0
                            start_time = time.time()
                            # Running the loop while file is received
                            while c <= int(file_size):
                                data = client_connection.recv(10240) # Able to up and down file 10GB
                                if not data:
                                    break
                                f.write(data)
                                c += len(data)

                            end_time = time.time()
                        
                        print("File transfer complete. Total time:", end_time - start_time)
                    break
                
                elif request == "quit":
                    break

if __name__ == "__main__":
    get_info()
    create_server()