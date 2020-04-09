#!/usr/bin/env python
# coding: utf-8

# In[15]:


import MySQLdb as mdb


# In[16]:


DBNAME = "dbtest"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"


# In[17]:


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


# In[21]:


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


# In[25]:


sqlQeueryForMap = """
                select c.crimeTypeID, ct.type, c.occuredAt, bl.topLeft_lat, bl.topLeft_lon, bl.topRight_lat, bl.topRight_lon, bl.bottomLeft_lat, bl.bottomLeft_lon, bl.bottomRight_lat, bl.bottomRight_lon 
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


# In[26]:


listOfListForMap = []

for row in tupleOfTupleForMap:
    listOfListForMap.append(list(row))
    
listOfListForMap


# In[ ]:




