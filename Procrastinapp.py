import sqlite3
import pandas.io.sql as sql

some_frame = ''
history = sqlite3.connect('history.txt')
table = sql.read_frame('select * from history',history)
table.to_csv('historyCSV.csv')