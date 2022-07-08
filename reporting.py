#!/usr/bin/python

# Work with an in-memory SQLite database and add help menu

from importlib.resources import path
from logging import root
import numbers
import os, sys, argparse, sqlite3

#Save in memory SQLite metadata
connection = sqlite3.connect(':memory:')

#Input variables and help menu
parser = argparse.ArgumentParser(description="This script searches a given folder for its files paths and sizes in MB.")
parser.add_argument("-p", "--path", type=str, help="Path of the folder")
parser.add_argument("-mb", "--mbytes", type=int, help="Maximun size of the files in MB , this is an optional parameter", default=10000000000000000, required=False)
parser.add_argument("-n", "--number", type=int, help="Number of files to be retrieved")
parser.add_argument("-t", "--filetype", type=str, help="file extension, this is an optional parameter", default="", required=False,)

args= parser.parse_args()

folder = args.path
maxsize = args.mbytes
numberfiles = args.number
extension = f"%{args.filetype}"


#print(folder, maxsize, numberfiles)

systemfiles = list()

#Example folder
#folder = /home/usuario/Data_Science_Courses

for paths, directories, files in os.walk(folder):
    for _file in files:
        full_path = os.path.join(paths, _file)
        bytes_size = os.path.getsize(full_path)
        mb_size = int(bytes_size/1024*2)
        row = (full_path, mb_size)
        systemfiles.append(row)


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


query = f'SELECT path, bytes FROM files WHERE path LIKE "{extension}" AND bytes<{maxsize} ORDER BY bytes DESC LIMIT({numberfiles})'
for i in cursor.execute(query):
    print(i)

