# Crime Map Visualizer 

This repo contains team Area51's crime map visualizer project for CS411, taught by Prof. Alawini in the Spring of 2020. 

## Dataset

We received this dataset from Champaign County Police, and we are grateful for it.

#### How CSV Files Were Created:

- We got the PDFs of the crimes committed at the University of Illinois at Urbana-Champaign from 2013 - 2019
- We converted the above dataset from .pdf to .doc files via this [website](pdf2doc.com)
- We copied the data of each .doc file to a new excel spreadsheet and cleaned the spreadsheet (to remove the page breaks)
- Lastly, we exported the excel files to .csv files

## MySQL 


### Setup

Setup Folder at the root of this repo has a text file which helps in installing WAMP server which comes with MySQL attached to Apache Server. For database operations, Python needs to be set-up.

### Loading Dataset

To Load the dataset, one needs to perform the following steps:
- Go to /SRC/DatabaseInteractionScripts
- Please update the following variables in all the python scripts, wherever applicable:
    The first three variables are the MySQL server credentials. If you haven't made any changes to the database after installation, then you don't need to change the values.
    - DBHOST (default: "localhost") - Host Name of the Server
    - DBPASS (default: "") - Password
    - DBUSER (default: "root") - Username
    
    Next variable that may need to be changed is the database name.
    - DBNAME (default: "dbtest") - Database Name
    
    Last variable that definitely needs a change is the *folder* path to the dataset.
    - csvFilePath - Folder path to the dataset; the dataset is in "\Src\Convert_CSV\Data"
    
- If the original dataset has been amended (that is YYYYnew.csv files), then one needs to rerun SplitOriginalDatasetInto3CSVs.ipynb script. This file combines all the crime log from all the years from 2013-2018 and splits into three CSVs which can be loaded into the Database. 
    - For now, those CSV filenames are hardcoded in the script, so one may write an additional function to automatically find the concerned CSVs. 
    - Also, this approach of creating three intermediate CSVs for each table out of the logs is not the most appropriate and efficient way to load data if the dataset is large, because it unnecessary. This optimisation be easily done by combining SplitOriginalDatasetInto3CSVs.ipynb and InsertTable.ipynb into single file.
    
- The following 2 files needs to be ran in sequence:
    - CreateTable.py (Please remember that it drops the table before creating it)

        CommandLine: ```python CreateTable.py```

    - InsertTable.py

        CommandLine: ```python InsertTable.py```
    
Now, you should have all the data inside your database. Login to the MySQL and check it.

Also, if you wish to reload the dataset, rerun the above two scripts, and you'd reset the whole dataset. If only specific table needs to be dropped, created and reloaded with data, then please use Jupyter Notebooks files or comment out the sections from the python file.

### Running Queries

To run any query on MySQL query using Python, please use the wrapper functions present in /SRC/DatabaseInteractionScripts/DatabaseHelperFunctions.py

It provides with the following functions:
- connectToDatabase(): Connect the script to MySQL database and returns the database object
- closeDatabase(db): Closes database
- executeSingleQuery(sqlquery): Executes single query whose sole purpose is to run without returning anything. For instance, DDL operation
- executeSingleQueryWhichReturns(sqlquery): Executes queries whose purpose is to return result. For instance, DML operation

### Interacting with the Website

GetDataForWebsiteMap.ipynb: Gets data from database to serve the website requests.

WebsiteToDB.ipynb: Performs queries on database such as insert, update, delete and select. Multiple wrapper functions are written to perform those tasks with various use cases. Please check the input/output instructions given and also it's looks pretty in Jupyter Notebook.

To run the Flask application, please follow the instructions on /Front_End/Setup_Instructions/Instructions.md

### Contributors: 
- [Yash Saboo](https://github.com/yashsaboo)
- [Jonathan Osei-Owusu](https://github.com/joseio)
- [Stephanie Lin](https://github.com/stephclin)
- [Xin Chen](https://github.com/xinc66)
