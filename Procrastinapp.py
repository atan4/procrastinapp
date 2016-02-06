import sqlite3
import csv
import pandas.io.sql as sql
from pandas import *


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



#newFile = open('cleanHistory.txt', 'w')
#newFile.write(urlList)
#newFile.close()
    
    