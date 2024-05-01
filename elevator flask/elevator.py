from flask import Flask, render_template

app = Flask(__name__)

current_floor = None
requested_floor = None

@app.route('/')
def elevator_ui():
    return render_template('elevator_ui.html', current_floor=current_floor, requested_floor=requested_floor)

@app.route('/update')
def receive_update():
    global current_floor, requested_floor
    # Here you would retrieve elevator data from the server
    # For demonstration, we'll set current_floor to 2nd floor and requested_floor to 12th floor
    current_floor = "2nd"
    requested_floor = "12th"
    return 'Update received'

def run_flask_app():
    app.run(debug=True)  # You can change debug to False for production

if __name__ == '__main__':
    run_flask_app()
