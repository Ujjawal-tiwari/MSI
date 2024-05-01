import socket
import threading
import math
import time
import matplotlib.pyplot as plt # type: ignore


# Initialize an empty list to store data points for plotting
data_points = []

def send_data():
    while True:
        try:
            # Connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('172.16.0.203', 704)
            client_socket.connect(server_address)

            # Generate a sinusoidal function with fluctuation
            t = time.time()
            data = math.sin(t) + 0.5 * math.sin(5 * t) + 0.2 * math.sin(10 * t)
            data_str = str(data)

            # Print the message before sending it
            print('Sending data:', data_str)

            # Add data point to the list for plotting
            data_points.append(data)

            # Send the data to the server
            client_socket.sendall(data_str.encode())

            # Close the connection
            client_socket.close()

            # Plot the graph
            plot_graph()

            time.sleep(1)  # Adjust the interval as needed

        except Exception as e:
            print("Error:", e)

# Function to plot the graph
def plot_graph():
    plt.clf()  # Clear the previous plot
    plt.plot(data_points, linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Sinusoidal Fluctuating Graph')
    plt.ylim(-2, 2)  # Adjust the y-axis limits as needed
    plt.draw()
    plt.pause(0.001)  # Pause to update the plot

# Function to start sending data
def start_csg_machine():
    while True:
        send_data()

# Start the CSG machine
start_csg_machine()
