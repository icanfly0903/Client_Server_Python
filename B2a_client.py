# -*- encoding: utf-8 -*-
import os
import socket
import time

# PORT = 9669 # Port to connect server

# Connect server
# def choose_server():
#     global SERVER_ADDRESS 
#     SERVER_ADDRESS = input("Please enter the Server address:")

# Create client


class create_client:
    def __init__(self, SERVER_ADDRESS, PORT):
        self.SERVER_ADDRESS = SERVER_ADDRESS
        self.PORT = PORT
        global client_sock
        print("Openning client socket...")
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        server_addr = (SERVER_ADDRESS, PORT)

        # Trying to connect to Server socket
        try:
            client_sock.connect(server_addr)
            print(f"=> Connected to {str(server_addr)}...")
        except:
            print("Unable to connect")
            exit(0)
    
    # Hiển thị tất cả các file đã upload lên server
    def lists(self):
        print("List files were uploaded to server:")
        for f in os.listdir("/Code/client<127.0.0.1><9669>/upload/"):
            print(f"+) {f}")
    
    # Upload file lên server 
    def upload_file(self):
        request = "upload"
        client_sock.send(request.encode("utf8"))
        print("=> Uploading file to server...")
        # Getting file details
        file_name = input("Upload file name:")
        file_size = os.path.getsize("/Code/client<127.0.0.1><9669>/upload/" + file_name)
        print(file_size)
        # Sending file_name and detail
        client_sock.send(file_name.encode("utf8"))
        client_sock.send(str(file_size).encode("utf8"))

        # Openning file and send data
        with open("/Code/client<127.0.0.1><9669>/upload/" + file_name, "rb") as f:
            c = 0
            # Starting the time capture 
            start_time = time.time()

            # Running loop while c != file_size 
            while c <= file_size:
                data = f.read(10240) 
                if not data:
                    break
                client_sock.sendall(data)
                c += len(data)

            # Ending the time capture 
            end_time = time.time()

        print("Tranfer file complete. Total time:", end_time - start_time)

    # Download file từ server 
    def download_file(self):   
        request = "download"
        client_sock.send(request.encode("utf8"))
        print("=> Downloading file from server...")
        
        # File name need to be downloaded
        file_name = input("Download file name:")
        client_sock.send(file_name.encode("utf8"))
        file_size = client_sock.recv(1024).decode("utf8")
        
        # Openning and reading file
        with open("/Code/client<127.0.0.1><9669>/download/" + file_name, "wb") as f:
            c = 0
            start_time = time.time()

            # Running the loop while file is received
            while c <= int(file_size):
                data = client_sock.recv(10240) # Able to up and down file 10GB
                if not data:
                    break
                f.write(data)
                c += len(data)

            end_time = time.time()

        print("File transfer complete. Total time:", end_time - start_time)
    
    def quit(self):
        request = "quit"
        client_sock.send(request.encode("utf8"))
        print("...close socket")
        client_sock.close()


if __name__ == "__main__":
    client = create_client('127.0.0.1', 9669)
    client.lists()
    while True:
        print(("-" * 10) + "OPTION" + ("-" * 10))
        print("\n1. Upload file to server")
        print("\n2. Download file from server")
        print("\n3. Close socket")
        print("\n" + "-" * 26)
        option = int(input("Please Enter Your Choice:"))
        if option == 1:
            client.upload_file()
        elif option == 2:
            client.download_file()
        elif option == 3:
            client.quit()
            break
        else:
            print("No option! Please Choose Again!")
        