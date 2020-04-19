#!/usr/bin/env python
# coding: utf-8

# In[66]:


import MySQLdb as mdb


# In[67]:


DBNAME = "dbtest"
DBHOST = "localhost"
DBPASS = ""
DBUSER = "root"


# In[68]:


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


# In[69]:


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


# ## Create BlockLocation Table

# In[70]:


# we are droping the table if it already exists
sqlqueryForDroppingTable_BlockLocation = "DROP TABLE IF EXISTS BlockLocation"
executeSingleQuery(sqlqueryForDroppingTable_BlockLocation)


# In[71]:


sqlqueryForCreatingTable_BlockLocation = """
                        CREATE TABLE BlockLocation
                        (
                         blockID int NOT NULL DEFAULT -1,
                         topLeft_lat real,
                         topLeft_lon real,
                         topRight_lat real,
                         topRight_lon real,
                         bottomLeft_lat real,
                         bottomLeft_lon real,
                         bottomRight_lat real,
                         bottomRight_lon real,
                         PRIMARY KEY (blockID)
                        );
                        """
    
executeSingleQuery(sqlqueryForCreatingTable_BlockLocation)


# ## Create CrimeType Table

# In[72]:


# we are droping the table if it already exists
sqlqueryForDroppingTable_CrimeType = "DROP TABLE IF EXISTS CrimeType"
executeSingleQuery(sqlqueryForDroppingTable_CrimeType)


# In[73]:


sqlqueryForCreatingTable_CrimeType = """
                        CREATE TABLE CrimeType
                        (
                         crimeTypeID int NOT NULL,
                         type varchar(255),
                         PRIMARY KEY (crimeTypeID)
                        );
                        """
    
executeSingleQuery(sqlqueryForCreatingTable_CrimeType)


# ## Create Crime Table

# In[74]:


# we are droping the table if it already exists
sqlqueryForDroppingTable_Crime = "DROP TABLE IF EXISTS Crime"
executeSingleQuery(sqlqueryForDroppingTable_Crime)


# In[75]:


sqlqueryForCreatingTable_Crime = """
                        CREATE TABLE Crime
                        (
                         incidentID varchar(20) NOT NULL,
                         reportedAt DateTime,
                         occuredAt DateTime,
                         disposition varchar(255),
                         crimeTypeID int NOT NULL,
                         PRIMARY KEY (incidentID),
                         FOREIGN KEY (crimeTypeID) REFERENCES CrimeType(crimeTypeID) 
                             ON DELETE CASCADE
                             ON UPDATE CASCADE
                        ); 
                        """
    
executeSingleQuery(sqlqueryForCreatingTable_Crime)


# ## Create happensAt Table

# In[76]:


# we are droping the table if it already exists
sqlqueryForDroppingTable_happensAt = "DROP TABLE IF EXISTS happensAt"
executeSingleQuery(sqlqueryForDroppingTable_happensAt)


# In[77]:


sqlqueryForCreatingTable_happensAt = """
                        CREATE TABLE happensAt
                        (
                         incidentID varchar(20) NOT NULL,
                         blockID int NOT NULL,
                         genLocation varchar(255),
                         FOREIGN KEY (incidentID) REFERENCES Crime(incidentID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                         FOREIGN KEY (blockID) REFERENCES BlockLocation(blockID)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE,
                         PRIMARY KEY (incidentID, blockID)
                        );
                        """
    
executeSingleQuery(sqlqueryForCreatingTable_happensAt)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




