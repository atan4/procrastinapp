import sqlite3
import csv
import pandas.io.sql as sql
from pandas import *
import datetime


def fromTextToPickle(email,filename):
    
    #some_frame = ''
    history = sqlite3.connect(filename)
    h = history.cursor()


    #query = """ 
    #CREATE TABLE pillow_hoodie 
    #(url LONGVARCHAR);"""
    ##h.execute(query)
    #h.commit()

    table = sql.read_frame('select * from urls["url"]',history)

    timeStamps = table[['last_visit_time','url']]
    timeDF = DataFrame(data = timeStamps, columns = ['last_visit_time','url','email'])
    timeDF['email'] = email
    timeDF.to_pickle(email.split('@')[0] + '_pickle.pkl')
    return timeDF

def dateTimeConversion(unixtime):
    #converts 17 digit time stamp
    time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=unixtime) 
    convertedTime = time.isoformat()
    return convertedTime


def main():
    pass


if __name__=='__main__':

    main()
