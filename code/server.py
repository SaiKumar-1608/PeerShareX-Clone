import socket
import threading

connected_clients = []  # List to store connected clients

def handle_client(client_socket, client_address):
    global connected_clients
    connected_clients.append(client_address)
    
    try:
        request = client_socket.recv(1024).decode()
        if request == "GET_CLIENT_LIST":
            client_list = "\n".join([f"{addr[0]}:{addr[1]}" for addr in connected_clients])
            client_socket.send(client_list.encode())
        elif request.startswith("REQUEST_FILE") or request.startswith("REQUEST_LARGE_FILE"):
            _, filename = request.split(" ", 1)
            filename = filename.strip()
            try:
                with open(filename, 'rb') as file:
                    print(f"Sending file '{filename}' to {client_address}...")
                    while True:
                        data = file.read(1024)  # Use a consistent small buffer size
                        if not data:
                            break
                        client_socket.sendall(data)
                    client_socket.send(b"<EOF>")  # Send EOF marker
                print(f"File '{filename}' sent to {client_address}.")
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
                client_socket.send(b"ERROR: File not found.")
        else:
            client_socket.send(b"ERROR: Unknown request.")
    except Exception as e:
        print(f"Error: {e}")
    finally: 
        client_socket.close()

def start_server(host='0.0.0.0', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":  # Fixed __name check
    start_server()