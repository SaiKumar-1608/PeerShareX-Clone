import socket
import os
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer

SERVER_IP = '192.168.78.159'  # Predefined server IP
SERVER_PORT = 5000
BUFFER_SIZE = 1024

# Global variable to store the current active streaming ID and status
active_streaming_id = None
stream_hosted = False

def display_client_menu():
    print("==============================")
    print("        CLIENT MENU           ")
    print("==============================")
    print("1. List Connected Clients")
    print("2. File Transfer")
    print("3. Large File Transfer")
    print("4. Stream Video")
    print("5. Exit")
    print("==============================")
    choice = input("Please select an option: ")
    return choice

def request_client_list():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.send("GET_CLIENT_LIST".encode())
            client_list = s.recv(4096).decode()
            if client_list:
                print("Connected Clients:\n" + client_list)
            else:
                print("No clients connected.")
    except (ConnectionRefusedError, socket.error) as e:
        print(f"Error fetching client list: {e}")

def file_transfer(transfer_choice, file_name):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            if transfer_choice == 'upload':
                if os.path.exists(file_name):
                    s.send(f"REQUEST_FILE {file_name}".encode())
                    with open(file_name, 'rb') as f:
                        while data := f.read(BUFFER_SIZE):
                            s.sendall(data)
                    s.send(b"<EOF>")  # Send EOF marker after upload
                    print(f"File '{file_name}' uploaded successfully.")
                else:
                    print(f"File '{file_name}' does not exist.")
            elif transfer_choice == 'download':
                s.send(f"REQUEST_FILE {file_name}".encode())
                with open(file_name, 'wb') as f:
                    while True:
                        data = s.recv(BUFFER_SIZE)
                        if not data:
                            break
                        if b"<EOF>" in data:
                            f.write(data.replace(b"<EOF>", b""))
                            break
                        f.write(data)
                print(f"File '{file_name}' downloaded successfully.")
    except (ConnectionRefusedError, socket.error) as e:
        print(f"File transfer error: {e}")

def large_file_transfer(transfer_choice, file_name):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            if transfer_choice == 'upload':
                if os.path.exists(file_name):
                    s.send(f"REQUEST_LARGE_FILE {file_name}".encode())
                    with open(file_name, 'rb') as f:
                        while True:
                            data = f.read(BUFFER_SIZE)
                            if not data:
                                break
                            s.sendall(data)
                    s.send(b"<EOF>")
                    print(f"Large file '{file_name}' uploaded successfully.")
                else:
                    print(f"File '{file_name}' does not exist.")
            elif transfer_choice == 'download':
                s.send(f"REQUEST_LARGE_FILE {file_name}".encode())
                with open(file_name, 'wb') as f:
                    while True:
                        data = s.recv(BUFFER_SIZE)
                        if not data:
                            break
                        if b"<EOF>" in data:
                            f.write(data.replace(b"<EOF>", b""))
                            break
                        f.write(data)
                print(f"Large file '{file_name}' downloaded successfully.")
    except (ConnectionRefusedError, socket.error) as e:
        print(f"Large file transfer error: {e}")

def stream_video():
    global active_streaming_id, stream_hosted

    print("1) Create Stream")
    print("2) Join Stream")
    choice = input("Please select an option (1-Create, 2-Join): ")

    if choice == '1':
        if stream_hosted:
            print("A stream is already active. Stop the current stream before creating a new one.")
            return

        streaming_id = input("Enter a unique streaming ID for others to join: ")
        video_file = input("Enter the name of the video file to stream: ")

        if not os.path.exists(video_file):
            print(f"Video file '{video_file}' not found.")
            return

        active_streaming_id = streaming_id
        stream_hosted = True

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Streaming</title>
</head>
<body>
    <h1>Streaming Video: {video_file} (ID: {streaming_id})</h1>
    <video width="640" height="360" controls>
        <source src="{video_file}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
</body>
</html>"""

        with open('stream_video.html', 'w') as html_file:
            html_file.write(html_content)

        os.chdir(os.path.dirname(os.path.abspath(video_file)))
        handler = SimpleHTTPRequestHandler
        httpd = HTTPServer(('localhost', 8000), handler)

        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        print(f"Streaming video '{video_file}' with ID '{streaming_id}' at http://localhost:8000/stream_video.html")
        webbrowser.open('http://localhost:8000/stream_video.html')

        input("Press Enter to stop streaming and return to the menu...")
        httpd.shutdown()
        stream_hosted = False
        active_streaming_id = None
        print("Stopped streaming.")

    elif choice == '2':
        if active_streaming_id is None:
            print("No stream is currently active. Please ask the host to start a stream.")
            return

        join_streaming_id = input("Enter the streaming ID to join: ")
        
        if join_streaming_id == active_streaming_id:
            print(f"Joining stream with ID '{join_streaming_id}'. Opening in browser...")
            webbrowser.open('http://localhost:8000/stream_video.html')
        else:
            print("Invalid streaming ID. Please check the ID and try again.")

def client_main():
    while True:
        choice = display_client_menu()
        if choice == '1':
            request_client_list()
        elif choice == '2':
            transfer_choice = "download"
            file_name = input("Enter the name of the file: ")
            file_transfer(transfer_choice, file_name)
        elif choice == '3':
            transfer_choice = "download"
            file_name = input("Enter the name of the large file: ")
            large_file_transfer(transfer_choice, file_name)
        elif choice == '4':
            stream_video()
        elif choice == '5':
            print("Exiting client...")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    client_main()
