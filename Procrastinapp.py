# Anne Schwartz, Adrianna Tan, Maja Svanberg
# ProcrastinApp.py
# Hack @ Smith
# 2o16-o2-o6

import sqlite3
import pandas.io.sql as sql
from pandas import *
import datetime
import urllib
<<<<<<< HEAD
import collections
from operator import itemgetter
=======
import classify
>>>>>>> 5015b8b64deec05fc92c8635a6e165a10b1775fc

def fromTextToPickle(email,filename):
    
    # translating the .txt file
    history = sqlite3.connect(filename)
    # connects sqlite into a dataframe
    h = history.cursor()

    # goes through and gets the url table from database
    table = sql.read_sql('select * from urls["url"]',history)

    # reduces table into two columns, time of visit, url
    timeStamps = table[['last_visit_time','url','visit_count']]

    # adds 'email' column to table
    timeDF = DataFrame(data = timeStamps, columns = ['last_visit_time','url','visit_count','email'])
    # sets email to input email
    timeDF['email'] = email

    # stores table as file
    timeDF.to_pickle(email.split('@')[0] + '_pickle.pkl')
    
    #converts unix time to readable times
    timeDF['last_visit_time'] = timeDF['last_visit_time'].apply(dateTimeConversion)
    
    # reduces URL to main webpage url
    def splitIt(url):
        if url.split('/')[0] == 'http:' or url.split('/')[0] == 'https:':
            return url.split('/')[2]
        else:
            return None
    
    timeDF['url'] = timeDF['url'].apply(splitIt)
    

    
    # sorts by visit count
    timeDF = timeDF.sort(['visit_count'],ascending = False)
    # returns dataframe
    return timeDF


def dateTimeConversion(unixtime):
    #converts 17 digit time stamp
    time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=unixtime) 
    # formats it into calendar format
    convertedTime = time.isoformat()
    return convertedTime

def addCategories(df):
    '''takes a dataframe and changes it, adds category'''
    df['category'] = df['url'].apply(classify.getType)

def fillDict():
    count = 1
    twentyFour = {}
    while count <= 24:
        twentyFour[count] = 0
        count += 1
    return twentyFour
    
dayDict = fillDict()

<<<<<<< HEAD
=======
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
    
>>>>>>> 5015b8b64deec05fc92c8635a6e165a10b1775fc

        
#def mostCommonTimes(email,filename):
#    for entry in fromTextToPickle(email,filename)['last_visit_time']:
#        for key in dayDict:
#            if key == int(entry.split('T')[1].split('.')[0].split(':')[0]):
#                dayDict[key] += 1
#    return dayDict



    


def main():
#    pass
#    print getHTML("https://github.com/aaronsw/html2text")

<<<<<<< HEAD


    df = fromTextToPickle('msvanberg@wellesley.edu', 'History.txt')
    
    #times = mostCommonTimes('msvanberg@wellesley.edu', 'History.txt')

    print df
=======
    #df = fromTextToPickle('msvanberg@wellesley.edu', 'History.txt')
    #dh = df.head()
    #addCategories(dh)
    #print dh
    times = mostCommonTimes('msvanberg@wellesley.edu', 'History.txt')
    sites = mostCommonSites('msvanberg@wellesley.edu', 'History.txt')
    #print len(sites)
    #print df
>>>>>>> 5015b8b64deec05fc92c8635a6e165a10b1775fc

    
if __name__=='__main__':

    main()
