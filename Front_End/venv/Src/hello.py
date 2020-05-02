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
sys.path.insert(0, os.path.abspath('Src/DatabaseInteractionScripts'))
import WebsiteToDB

app = Flask(__name__)
app.config['DEBUG'] = True

# Sources:
# https://github.
# com/shanealynn/async_flask
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


# =============================== FLASK: MAIN DATA ===============================

@app.route('/', methods=['POST', 'GET'])
def index():
    # only by sending this page first will the client be connected to the socketio instance
    crimeDBData  = sendDBData()
    # complexQ2Data = complexQuery2('3',"""'2015-01-01'""")
    # blueLightData = sendBluelightData()
    return render_template('track1index.html', crimeDBData=crimeDBData) #, blueLightData=blueLightData)


# TODO: Jonathan will add Xin's predictions to site
@app.route('/predicted')
def predicted():
    # Get (1) dictionary mapping block ID to coords and (2) dictionary mapping block ID to crime predictions
    blockDict, predictDict = getBlockAndPredictionDicts()
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('predicted.html', blockToCoord=blockDict, predictedDBData=predictDict)

# INSERT data into DB
@app.route('/insert/', methods=['POST'])
def insert():
    data = request.get_json()
    print('FROM JAVASCRIPT: ', data)
    res = WebsiteToDB.insertNewData({'incidentID': ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8)),
        'reportedAt': datetime.now().strftime(r"%Y-%m-%d %H:%M:%S"),
        'occuredAt': data['crimeDateTime'],
        'disposition': data['disposition'],
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

# EDIT data in DB
@app.route('/edit/', methods=['POST'])
def edit():
    data = request.get_json()
    print('FROM JAVASCRIPT: ', data)
    res = WebsiteToDB.updateDataUsingIncidentID(data['updateColumn'], data['incidentID'], data['newVal'])
    
    # Emit updated data if insertion succesful
    if res:
        print('editsuccessful')
        return render_template('track1index.html', crimeDBData=sendDBData())
    return None

# DELETE data from DB
@app.route('/delete/', methods=['POST'])
def delete():
    data = request.get_json()
    print('FROM JAVASCRIPT: ', data)

    res = WebsiteToDB.deleteData(data['deleteColumn'], data['deleteValue'])
    
    # Emit updated data if insertion succesful
    if res:
        print('deletion successful')
        return render_template('track1index.html', crimeDBData=sendDBData())
    return None

# SEARCH for data tuple in DB
@app.route('/search/', methods=['POST'])
def search():
    if request.method == 'POST':
        print('FROM JAVASCRIPT: ', request.form['search'])
        res = WebsiteToDB.searchData(request.form['search'])
        # Dynamically reaload if search succesful
        if res:
            print('search successful')
            return render_template('track1index.html', crimeDBData=sendDBData(), search_res=res)

    return None

# COMPLEX QUERY 2
@app.route('/query2/', methods=['POST'])
def query2():
    if request.method == 'POST':
        print("Executing Complex Query 2")
        data = request.get_json()
        numCrimes = str(data['numOfCrimes'])
        crimeAfterDate = str(data['crimeTime'])

        # get results of query
        query2CrimeList = complexQuery2(numCrimes, crimeAfterDate)
        # print(query2CrimeList)
        if query2CrimeList:
            return render_template('track1index.html', crimeDBData=sendDBData(), query2CrimeList=query2CrimeList)
    return None



# connect live thread
@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(randomNumberGenerator)

# disconnect thread 
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    global thread, thread_stop_event
    print('Client disconnected')
    # test_connect()
    # thread_stop_event.set()
    # thread.join()
    # print('All threads killed')


# =============================== DATABASE FUNCTIONS ===============================

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

# function to generate random numbers
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


# =============================== DATABASE QUERYING ===============================

# function to query DB for crime data and return as list of lists
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

    return listOfListForMap

# function for complex query 2
# numCrimes is the number of crimes to be shown
# afterDate is the date after which these crimes should occur
def complexQuery2(numCrimes, afterDate):
    query = """select ct.type as crimeType, count(c.incidentID) as numberOfCrimes
                        from Crime c
                        INNER JOIN
                        CrimeType ct ON
                        c.crimeTypeID = ct.crimeTypeID
                        INNER JOIN
                        happensAt h ON
                        c.incidentID = h.incidentID
                        where h.blockID != 0 and c.occuredAt >= """ + afterDate + """
                        group by ct.type
                        order by count(h.incidentID) desc
                        LIMIT """ + numCrimes

    print(query)
    
    queryTuples = executeSingleQueryWhichReturns(query)
    complexQueryList = []

    for row in queryTuples:
        crimeType = row[0]
        numCrimes = row[1]
        listRow = [crimeType, numCrimes]

        complexQueryList.append(listRow)
    
    print(complexQueryList)
    return complexQueryList



# function to query safecall DB and get blue light coordinates 
# def sendBluelightData():
#     blueLightQuery = """
#                 select lat, lon
#                 from 
#                 safecall
#                 """
#     queryTuple = executeSingleQueryWhichReturns(blueLightQuery)    
#     blueLightList = []
#     for row in queryTuple:
#         if None in row:
#             continue
        
#         lat = row[0]
#         lon = row[1]
#         blueLightList.append(lat)
#         blueLightList.append(lon)
    
#     return blueLightList



# Function to map block locations to block coords
def getBlockAndPredictionDicts():
    import csv 
    with open(r'\Src\DatabaseInteractionScripts\Data\BlockLocation.csv', 'r') as f:
        blockCoordDict = csv.DictReader(f)
    with open(r'\Src\DatabaseInteractionScripts\Data\predictions.csv', 'r') as f:
        predictionDict = csv.DictReader(f)
    return blockCoordDict, predictionDict
    


if __name__ == '__main__':
    socketio.run(app)