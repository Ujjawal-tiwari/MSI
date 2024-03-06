import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
server_address = ('localhost', 700)
client_socket.connect(server_address)

try:
    # Send a request to the server
    message = '<?xml version="1.0" encoding="UTF-8"?><request><data>ESPA-X message-ALERT go go run ! </data></request>'
    print('Sending:', message)
    client_socket.sendall(message.encode())

    # Receive response from the server
    response = client_socket.recv(1024).decode()
    print('Received:', response)

finally:
    # Clean up the connection
    client_socket.close()
