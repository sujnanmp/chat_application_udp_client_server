import socket
import threading

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define server address and port
server_address = ('127.0.0.1', 12345)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening for incoming connections...")

# List to store client connections
clients = []

# Function to broadcast messages to all connected clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Function to handle individual client connections
def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            message = message.decode()
            broadcast(message.encode(), client_socket)
        except:
            break

    clients.remove(client_socket)
    client_socket.close()

# Main server loop
while True:
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
