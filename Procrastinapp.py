# Anne Schwartz, Adrianna Tan, Maja Svanberg
# ProcrastinApp.py
# Hack @ Smith
# 2o16-o2-o6

import sqlite3
import pandas.io.sql as sql
from pandas import *
import datetime
import urllib
import collections
from operator import *
import classify
from ggplot import *

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
            return '/'.join(url.split('/')[:3])
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
    
def mostCommonTimes(email,filename):
    for entry in fromTextToPickle(email,filename)['last_visit_time']:
        for key in dayDict:
            if key == int(entry.split('T')[1].split('.')[0].split(':')[0]):
                dayDict[key] += 1
    return dayDict

def top3categories(df):
    '''takes a dataframe and changes it, adds category'''
    df['category'] = df['url'].apply(classify.getType)
    grouped = df['visit_count'].groupby(df['category']).sum()
    return grouped



def main():
#    pass
#    print getHTML("https://github.com/aaronsw/html2text")


    gg = ggplot(aes(x='Hour of the day', y = 'Amount of online activity (sites visited)'), \
               data=mostCommonTimes('msvanberg@wellesley.edu', 'History.txt')) +\
               geom_bar()    
    print gg
    #print df

    #df = fromTextToPickle('msvanberg@wellesley.edu', 'History.txt')
    #print top3categories(df.head())
#dh = df.head()
    #addCategories(dh)
    #print dh
    #times = mostCommonTimes('msvanberg@wellesley.edu', 'History.txt')
    #sites = mostCommonSites('msvanberg@wellesley.edu', 'History.txt')
    #print len(sites)
    #print df

if __name__=='__main__':

    main()
