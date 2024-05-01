import socket
import threading
import json

# Global list to store received data
received_data = []

def handle_client(connection, client_address):
    print('Connection from', client_address)

    while True:
        data = connection.recv(1024).decode()
        if not data:
            print('Client', client_address, 'disconnected.')
            break

        print('Received from', client_address, ':', data)

        # Append received data to the global list
        received_data.append({
            "client_address": client_address,
            "data": data
        })

    # Close the connection
    connection.close()

    # Save received data to JSON file
    with open('received_data.json', 'w') as json_file:
        json.dump(received_data, json_file, indent=4)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.123.35', 703)  # Change to your desired IP address and port
    server_socket.bind(server_address)
    server_socket.listen(15) 
    print('Server is listening on', server_address)

    while True:
        connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()

# Start the server
start_server()
