#!/usr/bin/env python
# coding: utf-8

# Assumptions:
#     1. The column names won't have any whitespace or period in it. If the CSV file columns have it, then it will be replaced with underscore.

# In[1]:


import MySQLdb as mdb
import csv
import pandas as pd


# In[2]:


DBNAME = "dbtest"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"


# In[3]:


csvFilePath = r"C:\Users\Yash\Desktop\Courses\CS411\Project Track 1\Src\DatabaseInteractionScripts\Data"


# In[4]:


def connectToDatabase():
    try:
        db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8', port=3308)
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


# In[5]:


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


# In[6]:


def getListOfInsertQueries(csvName, tableName):
    
    # Load CSV and get column names
    csvData = pd.read_csv(csvFilePath+"\\"+csvName)
    listOfcsvDataColumns = list(csvData.columns)
    
    # INSERT INTO Employee (Name, Email, Age) VALUES ('John', 'john@gmail.com', '25')
    
    columnNamesInQueryFormat = "("
    for i in listOfcsvDataColumns:
        columnNamesInQueryFormat = columnNamesInQueryFormat + i.replace(" ", "_").replace(".", "_") +"," #Replaces whitespace and period with underscore for column names
    columnNamesInQueryFormat = columnNamesInQueryFormat[:-1] + ")";

    partialInsertQuery = "INSERT INTO " + tableName + " " + columnNamesInQueryFormat + " VALUES"
    print(partialInsertQuery)
    
    listOfInsertQueries = []
    
    for i in range(0,csvData.shape[0]):
        betterHalfOfInsertQuery = "("
        for j in range(0,csvData.shape[1]):
#             print(betterHalfOfInsertQuery)
            data = str(csvData.at[i, listOfcsvDataColumns[j]])
            betterHalfOfInsertQuery = betterHalfOfInsertQuery + "'" + data + "',"
        betterHalfOfInsertQuery = betterHalfOfInsertQuery[:-1] + ")"
        listOfInsertQueries.append(partialInsertQuery + betterHalfOfInsertQuery)
    
    return listOfInsertQueries


# ## Insert into BlockLocation Table

# In[7]:


csvName = r"BlockLocation.csv"
tableName = "BlockLocation"
listOfInsertQueries = getListOfInsertQueries(csvName, tableName)
listOfInsertQueries


# In[8]:


for sqlqueryForInsertIntoTable_BlockLocation in listOfInsertQueries:
    executeSingleQuery(sqlqueryForInsertIntoTable_BlockLocation)


# In[9]:


# sqlqueryForInsertIntoTable_BlockLocation =   """
#                                     INSERT INTO Crime (incidentID, reportedAt, occuredAt, deposition) 
#                                     VALUES ('II1300026', '2013-1-1 1:39:00', '2013-1-1 1:39:00' ,'ARREST');
#                                     """
# executeSingleQuery(sqlqueryForInsertIntoTable_BlockLocation)


# In[ ]:





# ## Insert into CrimeType Table

# In[10]:


csvName = r"CrimeType.csv"
tableName = "CrimeType"
listOfInsertQueries = getListOfInsertQueries(csvName, tableName)
listOfInsertQueries


# In[11]:


for sqlqueryForInsertIntoTable_BlockLocation in listOfInsertQueries:
    executeSingleQuery(sqlqueryForInsertIntoTable_BlockLocation)


# In[ ]:





# ## Insert into Crime Table

# In[12]:


csvName = r"Crime.csv"
tableName = "Crime"
listOfInsertQueries = getListOfInsertQueries(csvName, tableName)
listOfInsertQueries


# In[13]:


for sqlqueryForInsertIntoTable_Crime in listOfInsertQueries:
    executeSingleQuery(sqlqueryForInsertIntoTable_Crime)


# ## Insert into happensAt Table

# In[14]:


csvName = r"happensAt.csv"
tableName = "happensAt"
listOfInsertQueries = getListOfInsertQueries(csvName, tableName)
listOfInsertQueries


# In[15]:


for sqlqueryForInsertIntoTable_happensAt in listOfInsertQueries:
    executeSingleQuery(sqlqueryForInsertIntoTable_happensAt)


# In[ ]:





# ## Insert into safeCall Table

# In[16]:


csvName = r"safeCall.csv"
tableName = "safeCall"
listOfInsertQueries = getListOfInsertQueries(csvName, tableName)
listOfInsertQueries


# In[17]:


for sqlqueryForInsertIntoTable_safeCall in listOfInsertQueries:
    executeSingleQuery(sqlqueryForInsertIntoTable_safeCall)


# In[ ]:





# ## Ignore

# In[45]:


# sqlqueryForInsertIntoTable_Crime =   """
#                                     INSERT INTO Crime (incidentID, reportedAt, occuredAt, deposition) 
#                                     VALUES ('II1300026', '2013-1-1 1:39:00', '2013-1-1 1:39:00' ,'ARREST');
#                                     """
# executeSingleQuery(sqlqueryForInsertIntoTable_Crime)


# In[46]:


# try:
#     db = mdb.connect(DBHOST, DBUSER, DBPASS, DBNAME, charset='utf8', port=3308)
#     print("Database Connected Successfully")

#     cur = db.cursor()
#     querysql = """
#     INSERT INTO Crime (incidentID, reportedAt, occuredAt, deposition) 
#     VALUES ('II1300026', '2013-1-1 1:39:00', '2013-1-1 1:39:00' ,'ARREST');
#     """
#     cur.execute(querysql)
#     #commit changes in the database
#     db.commit()
#     print("Data Inserted Successfully")
    
# except mdb.Error as e:
#     print(e)
#     db.rollback()
#     #roolback if there is an error
# db.close()


# In[ ]:




