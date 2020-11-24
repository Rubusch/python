#!/usr/bin/python

import MySQLdb

## open database connection
host = "localhost"
username = "testuser"
password = "test123"
dbname = "TESTDB"
db = MySQLdb.connect( host, username, password, dbname )

## prepare a cursor object using cursor() method
cursor = db.cursor()

## set up query
query = "SELECT VERSION()"

## execute SQL query using execute() method.
cursor.execute( query )

## fetch a single row using fetchone() method.
data = cursor.fetchone()
print "result : %s " % data

## disconnect from server
db.close()

print "READY.\n"


