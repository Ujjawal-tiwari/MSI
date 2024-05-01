from flask import Flask, render_template
import json
import threading
import socket
import plotly.graph_objs as go

app = Flask(__name__)

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

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Function to load data from the JSON file
def load_data():
    with open('received_data.json', 'r') as json_file:
        data = json.load(json_file)
    return data

# Function to generate and render the graph
def generate_graph(data):
    # Extracting required information from data
    clients = [entry['client_address'][0] for entry in data]
    data_counts = {client: clients.count(client) for client in set(clients)}

    # Create Plotly bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(data_counts.keys()), y=list(data_counts.values())))

    # Update layout
    fig.update_layout(
        title="Cardiac Rhythm Monitoring Graph",
        xaxis_title="Amplitude",
        yaxis_title="Time",
        # xaxis=dict(tickangle=45),
    )

    # Convert to HTML
    graph_html = fig.to_html(full_html=False)

    return graph_html

# Route for the home page
@app.route('/')
def home():
    data = load_data()
    graph_html = generate_graph(data)
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True)
