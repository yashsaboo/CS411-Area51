#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
Created on Thu Apr 9
@author: yashsaboo
"""


# 1. Check for sanity
# 2. Convert the msg into three csv columns
# 
#     i. find crimetypeid
#         a. Check if this crime is present or not. If not present, then add it to crimetype (first insert)
#     
#     ii. Find blockid
#         a. Call insert on crime
#     
#     iii. Call insert on happensAt

# # Input/Output Format

# ## Insert Format

# **Function Name**:  insertNewData(msg)
# 
# **Input**:          A dictionary variable with the following fields: incidentID, reportedAt, occuredAt, disposition, type, genLocation, lat, lon
# 
#                 For instance,
#                             {'incidentID': 'II1300563',
#                              'reportedAt': '20135-1-1 11:39:00',
#                              'occuredAt': '2013-1-1 11:39:00',
#                              'disposition': 'ARREST',
#                              'type': 'POSSESSION OF CANNABIS test5',
#                              'genLocation': 'CIRCLE K',
#                              'lat': '40.1081487',
#                              'lon': '-88.2293074'}
#                 Remember, all of them should of string type and have the exact format for dates and times.
#         
# **Output**:         True/False whether the new data was inserted successfully or not
# 
# **Example**: 
# 
#         msg = {}
#         msg["incidentID"] = "II1300563"
#         msg["reportedAt"] = '2013-1-1 11:39:00'
#         msg["occuredAt"] = '2013-1-1 11:39:00'
#         msg["disposition"] = "ARREST"
#         msg["type"] = "POSSESSION OF CANNABIS test5"
#         msg["genLocation"] = "CIRCLE K"
#         msg["lat"] = "40.1081487"
#         msg["lon"] = "-88.2293074"
#         insertNewData(msg)

# ## Delete Format

# **Function Name**: deleteData(columnNameOfDeleteRecord, valueOfDeleteRecord)
#     
# **Input**: 2 String values - columnNameOfDeleteRecord, valueOfDeleteRecord                
#     
# **Output**: True/False whether the new data was inserted successfully or not
#     
# **Example**: 
# 
#             columnNameOfDeleteRecord = "type"
#             valueOfDeleteRecord = "RAPE"
#             deleteData(columnNameOfDeleteRecord, valueOfDeleteRecord)

# # Update Format

# **Function Name**: updateData(columnNameOfUpdateRecord, oldValueOfUpdateRecord, newValueOfUpdateRecord)
#     
# **Input**: 3 String values - columnNameOfUpdateRecord, oldValueOfUpdateRecord, newValueOfUpdateRecord                
#     
# **Output**: True/False whether the new data was inserted successfully or not
#     
# **Example**: 
# 
#             columnNameOfUpdateRecord = "disposition"
#             oldValueOfUpdateRecord = "ARREST"
#             newValueOfUpdateRecord = "ARREST with Guns"
#             updateData(columnNameOfUpdateRecord, oldValueOfUpdateRecord, newValueOfUpdateRecord)

# # The Code

# In[1]:


import MySQLdb as mdb
import DatabaseHelperFunctions as dbhelp
import numpy as np


# In[2]:


csvFilePath = r"C:\Users\Yash\Desktop\Courses\CS411\Project Track 1\Src\Convert_CSV\Data"


# ### Sanity Checker

# In[3]:


def checkDateAndTimeSanity(str):
    #Check if both date and time are present
    arr = str.split(" ")
    if(len(arr)!=2):
        print("Hi")
        return False
    
    date = arr[0].split("-")
    time = arr[1].split(":")
    
    #Check if year has four numbers
    if(len(date[0])!=4):
        print("Hi2")
        return False
    
    #Check month
    if (int(date[1])>12) or (int(date[1])<1):
        return False
    
    #Check day
    if (int(date[2])>31) or (int(date[2])<1):
        return False
    
    #Check hour
    if (int(time[0])>24) or (int(time[0])<0):
        return False
    
    #Check min
    if (int(time[1])>60) or (int(time[1])<0):
        return False
    
    #Check sec
    if (int(time[2])>60) or (int(time[2])<0):
        return False
    
    return True
    

def checkSanity(msg):
    
    #Check if string doesn't have ' and .
    for key in msg:
        if key!="lat" and key!="lon":
            msg[key] = msg[key].replace("\'", "").replace(".", "")
    
    #Date and Time are in proper format
    if (not checkDateAndTimeSanity(msg["reportedAt"])):
        print("reportedAt")
        return False
    
    if (not checkDateAndTimeSanity(msg["occuredAt"])):
        print("occuredAt")
        return False
    
    return True


# ### Find CrimeTypeID

# In[4]:


def findCrimeTypeID_InsertIfNotPresent(crimeType):
    sqlQeueryForCheckingIDExist = """
                                select crimeTypeID from CrimeType where type="{type}"
                                """
    checkingIDResult = dbhelp.executeSingleQueryWhichReturns(sqlQeueryForCheckingIDExist.format(type = crimeType))

    #New Crime Type
    if len(checkingIDResult)==0:

        #Find new crimeTypeID
        sqlQeueryForFindingLastID = """
                    SELECT * FROM CrimeType ORDER BY crimeTypeID DESC LIMIT 1
                    """
        lastIDResult = dbhelp.executeSingleQueryWhichReturns(sqlQeueryForFindingLastID)
    #     print(lastIDResult)

        #Insert new crime type into the table
        sqlqueryForInsertIntoTable_CrimeType =   """
                                        INSERT INTO CrimeType (crimeTypeID,type) 
                                        VALUES("{crimeTypeID}","{type}")
                                        """
        querySuccessOrNot = dbhelp.executeSingleQuery(sqlqueryForInsertIntoTable_CrimeType.format(crimeTypeID = str(lastIDResult[0][0]+1), type = crimeType))
        
        if not querySuccessOrNot:
            return False
        
        return str(lastIDResult[0][0]+1)
    
    #Crime type exsits
    elif len(checkingIDResult)==1:
        print("crimeTypeID already present")
        return checkingIDResult[0][0]

    #Error
    else:
        print("Error in generating or finding crime type ID")
    
    return None


# ### Find blockID

# In[5]:


def search(lat, lon):
    block_raw = np.loadtxt(csvFilePath + "//" + 'BlockLocation.csv', delimiter = ',', skiprows = 1)
    block = np.zeros((50, 8))
    for i in range(50):
        block[int(block_raw[i,0]) - 1] = block_raw[i,1:] 
    
    index = 0
    for j in range(50):
        if((lat < block[j][0]) & (lat > block[j][6]) & (lon < block[j][3]) & (lon > block[j][1])):
            index = j + 1
    print(index)
    return index


# ## Insert New Data

# In[7]:


def insertNewData(msg):
    
    try:
        #Check sanity of the values
        saneOrNot = checkSanity(msg)
        if not saneOrNot:
            return False

        #Get blockID
        msg["blockID"] = search(float(msg["lat"]), float(msg["lon"]))

        #Get crimeTypeID
        msg["crimeTypeID"] = findCrimeTypeID_InsertIfNotPresent(msg["type"])
        if msg["crimeTypeID"]==None:
            return False
        
        # Insert into Crime Table
        sqlqueryForInsertIntoTable_Crime =   """
                                        INSERT INTO Crime (incidentID,reportedAt,occuredAt,disposition,crimeTypeID) 
                                        VALUES("{incidentID}","{reportedAt}","{occuredAt}","{disposition}","{crimeTypeID}")
                                        """
        querySuccessOrNot = dbhelp.executeSingleQuery(sqlqueryForInsertIntoTable_Crime.format(incidentID = msg["incidentID"], 
                                                                              reportedAt = msg["reportedAt"],
                                                                              occuredAt = msg["occuredAt"],
                                                                              disposition = msg["disposition"],
                                                                              crimeTypeID = msg["crimeTypeID"],
                                                                             ))
        if not querySuccessOrNot:
            return False

        # Insert into happensAt Table
        sqlqueryForInsertIntoTable_happensAt =   """
                                        INSERT INTO happensAt (incidentID,blockID,genLocation) 
                                        VALUES("{incidentID}","{blockID}","{genLocation}")
                                        """
        querySuccessOrNot = dbhelp.executeSingleQuery(sqlqueryForInsertIntoTable_happensAt.format(incidentID = msg["incidentID"], 
                                                                              blockID = msg["blockID"],
                                                                              genLocation = msg["genLocation"]
                                                                             ))
        if not querySuccessOrNot:
            return False
        
        print("Inserted the new row")
        return True
    except e:
        print("Couldn't insert the new row")
        print(e)
        return False


# In[12]:


# msg = {}
# msg["incidentID"] = "II1300563"
# msg["reportedAt"] = '2013-1-1 11:39:00'
# msg["occuredAt"] = '2013-1-1 11:39:00'
# msg["disposition"] = "ARREST"
# msg["type"] = "POSSESSION OF CANNABIS test5"
# msg["genLocation"] = "CIRCLE K"
# msg["lat"] = "40.1081487"
# msg["lon"] = "-88.2293074"
# msg


# In[13]:


# insertNewData(msg)


# ## Delete Data

# In[14]:


columnsOfCrimeType = ["type", "crimeTypeID"]
columnsOfCrime     = ["incidentID", "reportedAt", "occuredAt", "disposition"]
columnsOfhappensAt = ["genLocation"]


# In[16]:


def getTableName(columnName):
    if columnName in columnsOfCrimeType:
        return "CrimeType"
    
    elif columnName in columnsOfCrime:
        return "Crime"
    
    elif columnName in columnsOfhappensAt:
        return "happensAt"
    
    else:
        return None


# In[18]:


def deleteData(columnNameOfDeleteRecord, valueOfDeleteRecord):

    tableNameOfDeleteRecord = getTableName(columnNameOfDeleteRecord)
    if tableNameOfDeleteRecord == None:
        return False
    # Delete from Table
    sqlqueryForDeleteFromTable = "Delete from {tableName} where {columnName} = \"{value}\""

    querySuccessOrNot = dbhelp.executeSingleQuery(sqlqueryForDeleteFromTable.format(tableName = tableNameOfDeleteRecord, 
                                                                columnName = columnNameOfDeleteRecord,
                                                                value = valueOfDeleteRecord
                                                                ))
    if not querySuccessOrNot:
        return False
    else:
        return True


# In[19]:


# columnNameOfDeleteRecord = "type"
# valueOfDeleteRecord = "RAPE"
# deleteData(columnNameOfDeleteRecord, valueOfDeleteRecord)


# ## Update Data

# ### Only one column

# In[20]:


def updateData(columnNameOfUpdateRecord, oldValueOfUpdateRecord, newValueOfUpdateRecord):
    
    tableNameOfUpdateRecord = getTableName(columnNameOfUpdateRecord)
    if tableNameOfUpdateRecord == None:
        return False
    
    # Update Table
    sqlqueryForDeleteFromTable = "Update {tableName} set {columnName} = \"{newValue}\" where {columnName} = \"{oldValue}\""

    querySuccessOrNot = dbhelp.executeSingleQuery(sqlqueryForDeleteFromTable.format(tableName = tableNameOfUpdateRecord, 
                                                                columnName = columnNameOfUpdateRecord,
                                                                oldValue = oldValueOfUpdateRecord,
                                                                newValue = newValueOfUpdateRecord
                                                                ))
    if not querySuccessOrNot:
        return False
    else:
        return True


# In[23]:


# columnNameOfUpdateRecord = "disposition"
# oldValueOfUpdateRecord = "ARREST"
# newValueOfUpdateRecord = "ARREST with Guns"
# updateData(columnNameOfUpdateRecord, oldValueOfUpdateRecord, newValueOfUpdateRecord)


# ### Two columns