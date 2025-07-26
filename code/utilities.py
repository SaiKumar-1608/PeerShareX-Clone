#   
def receive_file(client_socket, filename):
    with open(filename, 'wb') as f:
        while True:
            bytes_read = client_socket.recv(1024)
            if not bytes_read:
                break
            f.write(bytes_read)
    print(f"Received file: {filename}")

def send_file(client_socket, filename):
    with open(filename, 'rb') as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break
            client_socket.send(bytes_read)
    print(f"Sent file: {filename}")
