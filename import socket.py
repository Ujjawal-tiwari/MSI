import socket
import threading

def handle_client(connection, client_address):
    try:
        print('Connection from', client_address)

        data = connection.recv(1024).decode()
        print('Received:', data)

        # Echo back the received data
        response = 'go'
        connection.sendall(response.encode())

    finally:
        connection.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 700)
server_socket.bind(server_address)
server_socket.listen(1)
print('ESPA-X server is listening on', server_address)

while True:
    connection, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()
