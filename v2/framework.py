from flask import Flask, render_template, request
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_request', methods=['POST'])
def send_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 700))

    try:
        message = '<?xml version="1.0" encoding="UTF-8"?><request><data>ESPA-X message-ALERT go go run ! </data></request>'
        print('Sending:', message)
        client_socket.sendall(message.encode())

        response = client_socket.recv(1024).decode()
        print('Received:', response)
        
        return response  # Return the received data to be displayed in the HTML template

    finally:
        client_socket.close()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
