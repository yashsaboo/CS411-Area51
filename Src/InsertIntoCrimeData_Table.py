import MySQLdb as mdb
import csv
import pandas as pd
 
# Connect to Database
DBNAME = "dbtest"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"
db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8', port=3308)

try:
    db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8', port=3308)
    print("Database Connected Successfully")

except mdb.Error as e:
    print(e)
    print("Database Not Connected Successfully")
 
# Insert into Database
csvFilePath = r"C:\Users\steph\Documents\School\Illinois\CS 411\Track 1\CS411-Area51\Src\Convert_CSV\Data\CSVs"
csvName = r"Partial Edited 2013.csv"

csvData = pd.read_csv(csvFilePath+"\\"+csvName)
listOfcsvDataColumns = list(csvData.columns)

# INSERT INTO Employee (Name, Email, Age) VALUES ('John', 'john@gmail.com', '25')
tableName = "CrimeData"

columnNamesInQueryFormat = "("
for i in listOfcsvDataColumns:
    columnNamesInQueryFormat = columnNamesInQueryFormat + i.replace(" ", "_") +"," #Replaces space with underscore for column names
columnNamesInQueryFormat = columnNamesInQueryFormat[:-1] + ")";

partialInsertQuery = "INSERT INTO " + tableName + " " + columnNamesInQueryFormat + " VALUES"

cur = db.cursor()
querysql = """
INSERT INTO Employee (Name, Email, Age) VALUES ('John', 'john@gmail.com', '25')
"""
try:
    for i in range(0,csvData.shape[0]):
        betterHalfOfInsertQuery = "("
        for j in range(0,csvData.shape[1]):
            data = csvData.at[i, listOfcsvDataColumns[j]].replace("\n", "") #Replaces newline feed
            betterHalfOfInsertQuery = betterHalfOfInsertQuery + "'" + data + "',"
        betterHalfOfInsertQuery = betterHalfOfInsertQuery[:-1] + ")"
        querysql = partialInsertQuery + betterHalfOfInsertQuery
        print(querysql)
        print()
        cur.execute(querysql)

    #commit changes in the database
    db.commit()
    print("Data Inserted Successfully")
except:
    db.rollback()
    #roolback if there is an error
 
db.close()