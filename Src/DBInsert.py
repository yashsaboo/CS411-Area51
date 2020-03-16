import MySQLdb as mdb
 
DBNAME = "area51"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"
db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8', port=3308)
cur = db.cursor()
querysql = """
INSERT INTO Employee (Name, Email, Age) VALUES ('John2', 'joh8n@gmail.com', '285')
"""
try:
    cur.execute(querysql)
    #commit changes in the database
    db.commit()
    print("Data Inserted Successfully")
except:
    db.rollback()
    #roolback if there is an error
 
db.close()