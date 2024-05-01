from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import socket
import threading
import json

app = Flask(__name__)
socketio = SocketIO(app)
server_address = ('192.168.123.35', 704)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# Flag to indicate whether to receive messages from the client
receive_messages_flag = True

def receive_messages():
    global receive_messages_flag
    while receive_messages_flag:
        try:
            # Receive messages from the client
            data = client_socket.recv(1024).decode()
            if data:
                # Check if the received data is JSON or XML
                try:
                    # Try to load data as JSON
                    json_data = json.loads(data)
                    # Write received JSON data to a file in static folder
                    with open('static/received_message.json', 'w') as json_file:
                        json.dump(json_data, json_file)
                    socketio.emit('message_update', {'message': json.dumps(json_data)})
                except ValueError:
                    # Handle XML data
                    socketio.emit('message_update', {'message': data})
        except Exception as e:
            print("Error receiving message:", e)
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/liftcall')
def liftcall():
    global receive_messages_flag
    try:
        receive_messages_flag = False
        message = "1"
        client_socket.sendall(message.encode())
        return render_template('liftcall.html')
    except Exception as e:
        return jsonify(error="Error initiating lift call")

@app.route('/send_request', methods=['POST'])
def send_request():
    try:
        pass
    except Exception as e:
        return jsonify(error="Error processing request")

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()
    socketio.run(app, debug=True, port=5001)
