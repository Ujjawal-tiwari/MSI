import socket
import xml.etree.ElementTree as ET
import time

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
server_address = ('192.168.123.35', 704)
client_socket.connect(server_address)

try:
    # Define a flag to indicate whether to send data or not
    send_data = True

    while send_data:
        # Set initial elevator position and ordered floor number
        elevatorPosition = 1
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
            # Construct XML message with elevator position and ordered floor number
            root = ET.Element('request')
            data = ET.SubElement(root, 'data')

            elevator_position_elem = ET.SubElement(data, 'elevatorPosition')
            elevator_position_elem.text = str(currentFloor)

            ordered_floor_number_elem = ET.SubElement(data, 'orderedFloorNumber')
            ordered_floor_number_elem.text = str(orderedFloorNumber)

            # Convert XML to string and send to the server
            message = ET.tostring(root, encoding='utf-8')
            print('Sending:', message)
            client_socket.sendall(message)

            # Update current floor based on iteration direction
            currentFloor += step

            # Wait for a short period before sending the next message (optional)
            time.sleep(4)

        # Construct XML message for the final position
        root = ET.Element('request')
        data = ET.SubElement(root, 'data')

        elevator_position_elem = ET.SubElement(data, 'elevatorPosition')
        elevator_position_elem.text = str(orderedFloorNumber)

        ordered_floor_number_elem = ET.SubElement(data, 'orderedFloorNumber')
        ordered_floor_number_elem.text = str(orderedFloorNumber)

        # Convert XML to string and send to the server
        message = ET.tostring(root, encoding='utf-8')
        print('Sending:', message)
        client_socket.sendall(message)

        # Wait for a short period before sending the next message (optional)
        time.sleep(1)

finally:
    # Clean up the connection
    client_socket.close()
