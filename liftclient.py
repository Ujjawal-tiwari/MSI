import socket
import json
import time

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
server_address = ('192.168.123.35', 704)
client_socket.connect(server_address)

try:
    # Define the specific trigger message
    trigger_message = "1"

    # Define a flag to indicate whether to send data or not
    send_data = False

    while True:
        # Receive response from the server
        response = client_socket.recv(1024).decode()
        print('Received:', response)

        # Check if the received message matches the trigger message
        if response.strip() == trigger_message:
            send_data = True
            break  # Break the loop and proceed to send data
        else:
            # Keep listening for the trigger message
            continue

    # Once trigger message received, continuously send data
    while send_data:
        # Set initial elevator position and ordered floor number
        elevatorPosition = 7
        orderedFloorNumber = 10

        # Compare elevator position and ordered floor number to determine the direction of iteration
        if elevatorPosition < orderedFloorNumber:
            step = 1  # Iterate forwards (+1)
        elif elevatorPosition > orderedFloorNumber:
            step = -1  # Iterate backwards (-1)
        else:
            # Already at the requested floor
            print("Elevator is already at the requested floor.")
            step = 0  # No need to iterate

        # Iterate over each floor from current position to ordered floor number
        currentFloor = elevatorPosition
        while currentFloor != orderedFloorNumber:
            # Construct JSON message with elevator position and ordered floor number
            message_data = {
                "elevatorPosition": currentFloor,
                "orderedFloorNumber": orderedFloorNumber
            }
            message_json = json.dumps(message_data)
            print('Sending:', message_json)
            client_socket.sendall(message_json.encode())

            # Receive response from the server if needed
            response = client_socket.recv(1024).decode()
            print('Received:', response)

            # Update current floor based on iteration direction
            currentFloor += step

            # Wait for a short period before sending the next message (optional)
            time.sleep(4)

        # Construct JSON message for the final position
        final_message_data = {
            "elevatorPosition": orderedFloorNumber,
            "orderedFloorNumber": orderedFloorNumber
        }
        final_message_json = json.dumps(final_message_data)
        print('Sending:', final_message_json)
        client_socket.sendall(final_message_json.encode())

        # Wait for a short period before sending the next message (optional)
        time.sleep(1)

finally:
    # Clean up the connection
    client_socket.close()
