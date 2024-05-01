import socket
import threading

last_received_message = ""


def handle_client(connection, client_address):
    global last_received_message
    try:
        print('Connection from', client_address)

        # Send the last received message to the new client
        if last_received_message:
            connection.sendall(last_received_message.encode())

        while True:
            data = connection.recv(1024).decode()
            if not data:
                break

            print('Received:', data)

            # Update the last received message
            last_received_message = data

            # Broadcast the message to all clients except the sender
            for conn in client_connections:
                if conn != connection:
                    conn.sendall(data.encode())

    finally:
        # Remove the client connection when it's closed
        client_connections.remove(connection)
        connection.close()

# List to store all client connections
client_connections = []

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('172.16.0.203', 704)
    server_socket.bind(server_address)
    server_socket.listen(5) 
    print('ESPA-X server is listening on', server_address)

    while True:
        connection, client_address = server_socket.accept()
        client_connections.append(connection)  
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()

# Start the server
start_server()
