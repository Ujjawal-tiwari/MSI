# espax_server.py
import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('localhost', 5003)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print('ESPA-X server is listening on', server_address)

while True:
    # Wait for a connection
    print('Waiting for a connection...')
    connection, client_address = server_socket.accept()

    try:
        print('Connection from', client_address)

        # Receive data from the client
        data = connection.recv(1024).decode()
        print('Received:', data)

        # Process the received message (add your logic here)

        # Send response back to the client
        response = '<?xml version="1.0" encoding="UTF-8"?><response><status>OK</status></response>'  # Example response
        connection.sendall(response.encode())

    finally:
        # Clean up the connection
        connection.close()
