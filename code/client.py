import socket
import os
import sys

SERVER_IP = '192.168.82.160'  # Predefined server IP
SERVER_PORT = 5000
BUFFER_SIZE = 1024

def display_client_menu():
    print("==============================")
    print("        CLIENT MENU           ")
    print("==============================")
    print("1. List Connected Clients")
    print("2. File Transfer")
    print("3. Large File Transfer")
    print("4. Exit")
    print("==============================")
    choice = input("Please select an option: ")
    return choice

def request_client_list():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.send("GET_CLIENT_LIST".encode())
        client_list = s.recv(4096).decode()
        print("Connected Clients:\n" + client_list)

def file_transfer(transfer_choice, file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        if transfer_choice == 'upload':
            if os.path.exists(file_name):
                s.send(f"REQUEST_FILE {file_name}".encode())
                with open(file_name, 'rb') as f:
                    while data := f.read(BUFFER_SIZE):
                        s.sendall(data)
                print(f"File '{file_name}' uploaded successfully.")
            else:
                print(f"File '{file_name}' does not exist.")
        elif transfer_choice == 'download':
            s.send(f"REQUEST_FILE {file_name}".encode())
            with open(file_name, 'wb') as f:
                while data := s.recv(BUFFER_SIZE):
                    f.write(data)
            print(f"File '{file_name}' downloaded successfully.")
    display_client_menu()

def large_file_transfer(transfer_choice, file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        if transfer_choice == 'upload':
            if os.path.exists(file_name):
                s.send(f"REQUEST_LARGE_FILE {file_name}".encode())
                with open(file_name, 'rb') as f:
                    while data := f.read(BUFFER_SIZE * 10):
                        s.sendall(data)
                print(f"Large file '{file_name}' uploaded successfully.")
            else:
                print(f"File '{file_name}' does not exist.")
        elif transfer_choice == 'download':
            s.send(f"REQUEST_LARGE_FILE {file_name}".encode())
            with open(file_name, 'wb') as f:
                while data := s.recv(BUFFER_SIZE * 10):
                    f.write(data)
            print(f"Large file '{file_name}' downloaded successfully.")
    display_client_menu()

def client_main():
    while True:
        choice = display_client_menu()
        if choice == '1':
            request_client_list()
        elif choice == '2':
            transfer_choice = input("Do you want to (upload/download) a file? ").lower()
            file_name = input("Enter the name of the file: ")
            file_transfer(transfer_choice, file_name)
        elif choice == '3':
            transfer_choice = input("Do you want to (upload/download) a large file? ").lower()
            file_name = input("Enter the name of the large file: ")
            large_file_transfer(transfer_choice, file_name)
        elif choice == '4':
            print("Exiting client...")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    client_main()