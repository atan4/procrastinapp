import sqlite3
import pandas.io.sql as sql
from pandas import *
import datetime
import urllib

def fromTextToPickle(email,filename):
    
    # translating the .txt file
    history = sqlite3.connect(filename)
    # connects sqlite into a dataframe
    h = history.cursor()

    # goes through and gets the url table from database
    table = sql.read_sql('select * from urls["url"]',history)

    # reduces table into two columns, time of visit, url
    timeStamps = table[['last_visit_time','url']]

    # adds 'email' column to table
    timeDF = DataFrame(data = timeStamps, columns = ['last_visit_time','url','email'])
    # sets email to input email
    timeDF['email'] = email

    # stores table as file
    timeDF.to_pickle(email.split('@')[0] + '_pickle.pkl')

    # returns dataframe
    return timeDF

def dateTimeConversion(unixtime):
    #converts 17 digit time stamp
    time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=unixtime) 
    # formats it into calendar format
    convertedTime = time.isoformat()
    return convertedTime

def getHTML(url):
    """Takes a url and returns a string version of the html file"""
    page = urllib.urlopen(url).read()
    return page

def main():
#    pass
#    print getHTML("https://github.com/aaronsw/html2text")



    df = fromTextToPickle('msvanberg@wellesley.edu', 'History.txt')
    df['last_visit_time'] = df['last_visit_time'].apply(dateTimeConversion)
    print df
    
if __name__=='__main__':

    main()
