import MySQLdb as mdb
 
DBNAME = "dbtest"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"
 
try:
    db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8', port=3308)
    print("Database Connected Successfully")

    cur = db.cursor()
 
    # we are droping the table if it already exists
    cur.execute("DROP TABLE IF EXISTS Employee")
 
    sqlquery = """
    CREATE TABLE Employee (
    Name CHAR(20) NOT NULL,
    Email CHAR(20),
    Age INT
    )
 
    """
    cur.execute(sqlquery)
    print("Table Created Successfully")
    db.close()
 
except mdb.Error as e:
    print(e)
    print("Database Not Connected Successfully")