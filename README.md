# 🔗 PeerConnectX

A lightweight and secure peer-to-peer file sharing system built using Python socket programming. This application allows two or more devices on the same network to exchange files without relying on a centralized server — enabling fast, efficient, and simple local file sharing.

---

## 📌 Overview

**PeerConnectX** is designed to demonstrate the core principles of distributed systems and networking. It uses socket programming to facilitate peer-to-peer file transmission over TCP, simulating a minimal BitTorrent-like protocol for secure local file sharing.

This project can serve as a base for understanding:
- Peer-to-peer communication
- TCP-based file transfer
- Network programming with Python
- Basics of distributed system behavior

---

## 📂 Repository StructureInstallation and Usage

```text
PeerConnectX/
├── client.py         # Script for connecting to server and sending files
├── server.py         # Script for receiving files from a peer
├── utils.py          # Common helper functions (if applicable)
├── config.py         # Configuration constants (e.g., IP, port)
├── README.md         # Project documentation
└── requirements.txt  # Required Python packages (if any)
```

## Installation and Usage

## Prerequisites
-Python 3.6 or higher
-Two or more devices on the same local network (LAN/Wi-Fi)

## Installation
1. Clone the repository:
```bash
  git clone https://github.com/YOUR_USERNAME/PeerConnectX.git
  ```
2. Navigate to the project directory:
   ```bash
   cd PeerShareX-Clone
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
    1. On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    2. On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
5. Install dependencies:
```bash
  pip install -r requirements.txt
  ```

## Code Details
1. 📥 server.py – File Receiver
  This script starts a TCP socket server to listen for incoming file transfers.

  How to Run:
  ```bash
    python server.py
    ```
  🔹 What it does:
  Binds to a predefined port (e.g., 5000)
  
  Waits for a connection from a peer
  
  Receives the file and saves it locally (e.g., in a received_files/ folder)

2. 📤 client.py – File Sender
  This script connects to a server/peer and sends a selected file over TCP.
  
  How to Run:
  ```bash
    python client.py
    ```
  🔹 What it does:
  Prompts the user to enter the server's IP address (the receiver)
  
  Allows the user to select a file to send
  
  Sends the file in chunks over TCP and prints progress
  
  ⚠ Make sure the IP address entered matches the one of the machine running server.py.

3. utilities.py (Optional, if present)
  Contains helper functions for:
  
  File size formatting
  
  Chunk-wise file reading
  
  Progress bar display during transfer
  
  📁 Example File Transfer Output
  text
  Copy
  Edit
  [Server] Listening on port 5000...
  [Client] Connected to 192.168.0.105
  [Client] Sending: project.zip (2.3 MB)
  [Server] Receiving: project.zip
  [Server] File saved as ./received_files/project.zip
  [Client] File sent successfully!
```

## Conclusion
  This project demonstrates the basic structure of a peer-to-peer system using raw socket programming. It's designed to help students and developers understand how P2P file sharing works under the hood and can be extended to support advanced features like:
  
  -Encryption
  -Peer discovery
  -GUI interface
  -Multi-peer broadcasting

## License
  This project is licensed under the MIT License.
  You are free to use, modify, and distribute it with proper attribution.
