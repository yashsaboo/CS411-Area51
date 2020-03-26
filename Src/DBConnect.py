import MySQLdb as mdb
 
DBNAME = "area51"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"
 
try:
    db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8', port=3308)
    print("Database Connected Successfully")

    cur = db.cursor()
 
    # we are droping the table if it already exists
    cur.execute("DROP TABLE IF EXISTS Crime")
 
    sqlquery = """
    CREATE TABLE Crime
    (
        incidentID int NOT NULL AUTO_INCREMENT,
        reportedAt DateTime,
        occuredAt DateTime,
        deposition varchar(255),
        crimeTypeID int NOT NULL,
        PRIMARY KEY (incidentID),
        FOREIGN KEY (crimeTypeID) REFERENCES CrimeType(crimeTypeID)
    ) 
    """
    cur.execute(sqlquery)
    print("Table Created Successfully")
    db.close()
 
except mdb.Error as e:
    print(e)
    print("Database Not Connected Successfully")