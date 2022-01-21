## Notes: Lecture 4 SQL, Models, and Migrations  
SQL: Structured Query Language, used to interact with databases  
Django uses SQLAlchemy, a translation layer between SQL and Django/Python  
Migrations: updating database in response to changes in the database model  

```code for tabs: &emsp;```

## SQL
Data gets stored in tables, in rows and columns. Columns are
fields/attributes/features, some fact about the entity being stored. Rows are
individual entities being stored.  
Database management systems: MySQL, PostgreSQL, SQLite  
Often separated onto a separate server (except: SQLite, a database in a file)  
SQLite types: Text, Numeric(bool, facts represented as a number but not
necessairily a number), Integers, Real (floats), BLOB (Binary Large OBject)  
MySQL types: Char, Varchar, SmallInt, Int, BigInt, Float, Double, etc.  


## Tables
Creating a table:  
```CREATE TABLE tablename (```  
&emsp;```colName TYPE CONSTRAINT,```  
&emsp;```id INT PRIMARY KEY AUTOINCREMENT,```  
&emsp;```someField TEXT NOT NULL,```  
&emsp;```etc INTEGER```  
```);```  
Some constraints: Check, Default, Not Null, Primary Key, Foreign Key, Unique  

Adding data:  
```INSERT INTO tablename (colname someField etc) ```  
```VALUES ("data", "moredata", 1);```  


## SQL Queries
Getting data:  
```SELECT * FROM tablename;``` Gets all the data from tablename  
Filter by columns: ```SELECT column1, column2, columnN;```  
Filter by rows: ```SELECT * FROM tablename WHERE condition1 AND condition2;```  

SQLite CLI pretty formatting: ```.mode columns```, ```.headers yes```  

Wildcard:  
Select everything where "a" is somewhere in the condition:  
```SELECT * FROM table WHERE condition LIKE "%a%";```  
Other fuctions: Average, Count, Max, Min, Sum, etc.  

Updating data:  
```UPDATE table SET column = newvalue WHERE conditions;```  
Deleting data:  
```DELETE FROM table WHERE conditions;```  
Other clauses:  
LIMIT (limit # of results)  
ORDER BY condition  
GROUP BY
(consolidate results)  
HAVING (a condition on GROUP BY)  
etc.

However Django/SQLAlchemy typically writes our SQL code (in this course) 

Normalizing data: reducing redundancy, simplifying & clarifying your representations   

## Joining Tables  
The purpose of relational databases is to relate different entities together
into a coherent mapping of some system.  

Inner Join: Get data from all the entities that exist in every JOINed table   
```SELECT column1, column 2 FROM table1 JOIN table2 ON table1.key1 = table2.key1;```  

Indexes: an additional data structure to make queries more efficient  
```CREATE INDEX indexName ON someTable(someColumn);```  

SQL Injection attack: if you fail to abstract or escape your data, an attacker
may break your code.  
Race conditions: In high-throughput applications, there might be unexpected I/O
conditions. Can by solved by locking I/O transactions.  


## Django Models



## Migrations



## Shell



## Django Admin



## Many-to-Many Relationships



## Users
