#Tihs will be my primary simulator which will act like a healthcare device for now which in sending a Message in xml format,using socket over local host ip.



import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
server_address = ('192.168.123.35', 704)
client_socket.connect(server_address)

try:
    # Send a request to the server
    message = '<?xml version="1.0" encoding="UTF-8"?><request><data>Patient Ayush Agrawal jain ,bearing ID P132a floor 2 is suspected with cardiac arrest, Do you want to call elevator control System to block the access ? it will arrange lift for you on high priority . </data></request>'
    print('Sending:', message)
    client_socket.sendall(message.encode())

    # Receive response from the server
    response = client_socket.recv(1024).decode()
    print('Received:', response)

finally:
    # Clean up the connection
    client_socket.close()
