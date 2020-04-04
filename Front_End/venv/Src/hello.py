from flask import Flask, redirect, url_for, request, render_template
from flask_socketio import SocketIO, emit
from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__)
app.config['DEBUG'] = True

# Sources:
# https://github.com/shanealynn/async_flask
# https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/

# turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()


def randomNumberGenerator():
    """
    Generate a random number every 1 second and emit to a socketio instance (broadcast)
    Ideally to be run in a separate thread?
    """
    # infinite loop of magical random numbers
    print("Making random numbers")
    while not thread_stop_event.isSet():
        number = round(random()*100, 3)
        print(number)
        socketio.emit('newnumber', {'number': number}, namespace='/test')
        socketio.sleep(5)


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('track1index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)

# socketio = SocketIO(app)


# @app.route('/', methods=['POST', 'GET'])
# def home():
#     # return 'hello world'
#     return render_template('track1index.html')

# # Decorator to catch an event called "my event":
# @socketio.on('my event', namespace='/test')
# # test_message() is the event callback function.
# def test_message(message):
#     # Trigger a new event called "my response"
#     emit('my response', {'data': 'got it!'})
#     # that can be caught by another callback later in the program.


# @app.route('/success/<name>')
# def success(name):
#     return 'welcome %s' % name


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     err = ''
#     try:
#         if request.method == "POST":
#             attempted_username = request.form['username']
#             attempted_password = request.form['password']
#             if attempted_username == "admin" and attempted_password == "password":
#                 return redirect(url_for('success', name='admin'))
#             else:
#                 err = "Invalid credentials. Try Again."
#         return render_template('login.html')

#     except Exception as e:
#         return render_template("login.html", error=err)

#

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app)
