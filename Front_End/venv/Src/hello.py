from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_socketio import SocketIO, emit
from threading import Thread, Event
from datetime import datetime
from random import random
from time import sleep
import MySQLdb as mdb
import string
import secrets
import sys
import os
sys.path.insert(0, os.path.abspath('Src/Convert_CSV'))
import WebsiteToDB

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

# GLOBAL DB variables
DBNAME = "dbtest"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"


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


# -------------------- main page data ------------------------
@app.route('/', methods=['POST', 'GET'])
def index():
    # only by sending this page first will the client be connected to the socketio instance
    crimeDBData = sendDBData()
    return render_template('track1index.html', crimeDBData=crimeDBData)
    # return redirect(url_for('predicted'))


# TODO: Jonathan will add Xin's predictions to site
@app.route('/predicted')
def predicted():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('predicted.html')

# To rec'v data passed from Javascript
@app.route('/insert/', methods=['POST'])
def insert():
    data = request.get_json()
    print('FROM JAVASCRIPT: ', data)
    res = WebsiteToDB.insertNewData({'incidentID': ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
        'reportedAt': datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"),
        'occuredAt': data['crimeDateTime'],
        'disposition': 'ARREST',
        'type': data['crimeType'],
        'genLocation': 'CIRCLE K',
        'lat': data['lat'],
        'lon': data['lon']})
    
    # Emit updated data if insertion succesful
    if res:
        print('insertion successful')
        # socketio.emit('newdata', {'newdata': sendDBData()}, namespace='/test')
        return render_template('track1index.html', crimeDBData=sendDBData())
    # return jsonify(status="success", data=data)
    return None


@app.route('/edit/', methods=['POST'])
def edit():
    data = request.get_json()
    print('FROM JAVASCRIPT: ', data)
    # res = WebsiteToDB.updateData(data['crimeTypeID'], data['oldVal'], data['newVal'])

    res = WebsiteToDB.updateDataUsingIncidentID(data['updateColumn'], data['incidentID'], data['newVal'])
    
    # Emit updated data if insertion succesful
    if res:
        print('editsuccessful')
        # socketio.emit('newdata', {'newdata': sendDBData()}, namespace='/test')
        return render_template('track1index.html', crimeDBData=sendDBData())
    # return jsonify(status="success", data=data)
    return None

@app.route('/delete/', methods=['POST'])
def delete():
    data = request.get_json()
    print('FROM JAVASCRIPT: ', data)

    res = WebsiteToDB.deleteData(data['deleteColumn'], data['deleteValue'])
    
    # Emit updated data if insertion succesful
    if res:
        print('deletion successful')
        # socketio.emit('newdata', {'newdata': sendDBData()}, namespace='/test')
        return render_template('track1index.html', crimeDBData=sendDBData())
    # return jsonify(status="success", data=data)
    return None

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)


# ---------------------- DATABASE FUNCTIONS -----------------------------


def connectToDatabase():
    try:
        db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME,
                         charset='utf8', port=3308)
        print("Database Connected Successfully")
        return db
    except mdb.Error as e:
        print(e)
        print("Database Not Connected Successfully")
        return None


def closeDatabase(db):
    try:
        db.close()
        print("Database Closed Successfully")
    except mdb.Error as e:
        print(e)
        print("Database Not Closed Successfully")


def executeSingleQuery(sqlquery):

    db = connectToDatabase()

    try:
        cur = db.cursor()

        # execute query
        cur.execute(sqlquery)
        print("Query Successfully Executed")

        db.commit()

    except mdb.Error as e:
        print(e)
        print("Query Not Successfully Executed" + sqlquery)

    closeDatabase(db)


def executeSingleQueryWhichReturns(sqlquery):

    db = connectToDatabase()

    try:
        cur = db.cursor()

        # execute query
        number_of_rows = cur.execute(sqlquery)
        result = cur.fetchall()
        print("Query Successfully Executed and Fetched")

        db.commit()

    except mdb.Error as e:
        print(e)
        print("Query Not Successfully Executed and Fetched" + sqlquery)

    closeDatabase(db)

    return result

# function to send DB as list of lists


def sendDBData():

    sqlQeueryForMap = """
                    select c.incidentID, ct.type, c.occuredAt, bl.topLeft_lat, bl.topLeft_lon, bl.topRight_lat, bl.topRight_lon, bl.bottomLeft_lat, bl.bottomLeft_lon, bl.bottomRight_lat, bl.bottomRight_lon 
                    from 
                    Crime c
                    INNER JOIN
                        CrimeType ct ON
                        c.crimeTypeID = ct.crimeTypeID
                    INNER JOIN
                        happensAt h ON
                        c.incidentID = h.incidentID
                    INNER JOIN
                        BlockLocation bl ON
                        h.blockID = bl.blockID;  

                    """
    tupleOfTupleForMap = executeSingleQueryWhichReturns(sqlQeueryForMap)

    listOfListForMap = []

    for row in tupleOfTupleForMap:
        if None in row:
            continue

        crimeID = row[0]
        crimeType = row[1]
        # print("row:", row)
        dateTimeList = [row[2].year, row[2].month,
                        row[2].day, row[2].hour, row[2].minute]
        coord1 = row[3]
        coord2 = row[4]
        coord3 = row[5]
        coord4 = row[6]
        coord5 = row[7]
        coord6 = row[8]
        coord7 = row[9]
        coord8 = row[10]
        listRow = [crimeID, crimeType, dateTimeList, coord1,
                   coord2, coord3, coord4, coord5, coord6, coord7, coord8]
        listOfListForMap.append(listRow)

    # listOfListForMap

    return listOfListForMap


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global thread, thread_stop_event
    print('Client disconnected')
    # test_connect()
    # thread_stop_event.set()
    # thread.join()
    # print('All threads killed')


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
