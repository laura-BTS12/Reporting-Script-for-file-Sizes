#!/usr/bin/python

from logging import root
import os, sys

#Example folder
#folder = '/home/usuario/Data_Science_Courses'
print("This script searches a given folder for its files paths and sizes.")
folder = input('Which is the path of the folder you want to search? ')
maxsize = input('What is the maximun size of the files to be reported? ')
numberfiles = input ('How many files you want to retrieve? ')
print(folder)
systemfiles = list()

for path, directories, files in os.walk(folder):
    for _file in files:
        full_path = os.path.join(path, _file)
        size = os.path.getsize(full_path)
        row = (full_path, size)
        systemfiles.append(row)


# Work with an in-memory SQLite database again
import sqlite3
connection = sqlite3.connect(':memory:')

# Create a table again for holding a path and size, just like before
table = 'CREATE TABLE files (id integer primary key, path TEXT, bytes INTEGER)'
cursor = connection.cursor()
cursor.execute(table)
connection.commit()

for metadata in systemfiles:
    query = 'INSERT INTO files(path, bytes) VALUES(?, ?)'
    # the execute() method accepts a query and optionally a tuple with values 
    # corresponding to the question marks in VALUES
    cursor.execute(query, metadata)
    connection.commit()


query = f'SELECT path, bytes FROM files WHERE bytes<{maxsize} ORDER BY bytes DESC LIMIT({numberfiles})'
for i in cursor.execute(query):
    print(i)