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
    
    #converts unix time to readable times
    timeDF['last_visit_time'] = timeDF['last_visit_time'].apply(dateTimeConversion)

    # returns dataframe
    return timeDF

def dateTimeConversion(unixtime):
    #converts 17 digit time stamp
    time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=unixtime) 
    # formats it into calendar format
    convertedTime = time.isoformat()
    return convertedTime

def fillDict():
    count = 1
    twentyFour = {}
    while count <= 24:
        twentyFour[count] = 0
        count += 1
    return twentyFour
    
dayDict = fillDict()

def mostCommonTimes(email,filename):
    for entry in fromTextToPickle(email,filename)['last_visit_time']:
        for key in dayDict:
            if key == int(entry.split('T')[1].split('.')[0].split(':')[0]):
                dayDict[key] += 1
    return dayDict

def mostCommonSites(email,filename):
    popularDict = {}
    for url in fromTextToPickle(email,filename)['url']:
        if url.split('/')[0] == 'http:' or url.split('/')[0] == 'https:' and url.split('/')[2] not in popularDict:
            popularDict[url.split('/')[2]] = 0
     
    return popularDict


def mostCommonSitesFilled(email,filename):
    for url in fromTextToPickle(email,filename)['url']:
        for key in mostCommonSites(email,filename).keys():
            if url.split('/')[0] == 'http:' or url.split('/')[0] == 'https:' and url.split('/')[2] == key: 
                popularDict[key] += 1   
    



def main():
#    pass
#    print getHTML("https://github.com/aaronsw/html2text")



    df = fromTextToPickle('msvanberg@wellesley.edu', 'History.txt')
    times = mostCommonTimes('msvanberg@wellesley.edu', 'History.txt')
    sites = mostCommonSites('msvanberg@wellesley.edu', 'History.txt')
    print len(sites)
    #print df

    
if __name__=='__main__':

    main()
